#!/opt/homebrew/bin/python3.10
import os
import sys
import subprocess
import ctypes
import netifaces
import ipaddress
from scapy.all import ARP, Ether, srp, get_if_addr, get_if_hwaddr
import requests
from tabulate import tabulate
from colorama import Fore, Style
import socket
import time
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, SpinnerColumn
from threading import Thread
import ua_generator  # for robust randomized browser headers
import csv

CSV_FILENAME = "/Users/pawankoli/Python/HOME/knowndevices.csv"

def load_known_devices(filename=CSV_FILENAME):
    """
    Loads known MAC-to-vendor mappings from a CSV file (headers: MAC,Vendor).
    If the file doesn't exist, it creates one with a header.
    Returns a dictionary mapping MAC addresses (colon-separated, lowercase) to vendor names.
    """
    devices = {}
    if not os.path.isfile(filename):
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["MAC", "Vendor"])
            writer.writeheader()
        return devices
    try:
        with open(filename, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                mac = row.get("MAC", "").strip().lower()
                vendor = row.get("Vendor", "").strip()
                if mac:
                    devices[mac] = vendor
    except Exception as e:
        print(f"Error loading CSV file: {e}")
    return devices

def cache_vendor(mac, vendor, filename=CSV_FILENAME):
    """
    Appends a new MAC-to-vendor mapping to the CSV file and updates the known_devices dict.
    """
    try:
        with open(filename, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["MAC", "Vendor"])
            writer.writerow({"MAC": mac, "Vendor": vendor})
    except Exception as e:
        print(f"Error caching vendor for {mac}: {e}")

# Load known devices into a global dictionary.
known_devices = load_known_devices()

def ensure_admin():
    """
    Ensures the script is running with administrative privileges.
    On Windows, re-launches itself with elevated rights if not already.
    On POSIX systems, attempts to re-run using sudo.
    """
    if os.name == "nt":
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            is_admin = False
        if not is_admin:
            script = sys.argv[0]
            params = " ".join(sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script + " " + params, None, 1)
            sys.exit(0)
    else:
        if os.geteuid() != 0:
            sudo_password = "9301\n"  # Replace with your sudo password (insecure)
            command = ["sudo", "-S", sys.executable] + sys.argv
            proc = subprocess.Popen(command, stdin=subprocess.PIPE)
            proc.communicate(sudo_password.encode())
            sys.exit(0)

def get_default_interface():
    """
    Automatically detects the default network interface using netifaces.
    Returns the interface name or None if not found.
    """
    gateways = netifaces.gateways()
    default_gateway = gateways.get("default", {})
    if netifaces.AF_INET in default_gateway:
        return default_gateway[netifaces.AF_INET][1]
    return None

def get_network_range(interface):
    """
    Determines the local network range based on the given interface.
    Returns a CIDR string (e.g., "192.168.1.0/24") or None on failure.
    """
    try:
        iface_info = netifaces.ifaddresses(interface)
        ipv4_info = iface_info.get(netifaces.AF_INET, [{}])[0]
        local_ip = ipv4_info.get("addr")
        netmask = ipv4_info.get("netmask")
        if local_ip and netmask:
            network = ipaddress.IPv4Network(f"{local_ip}/{netmask}", strict=False)
            return str(network)
        return None
    except Exception as e:
        print(f"Error detecting network range: {e}")
        return None

def format_mac(mac):
    """
    Converts the MAC address into the standard colon-separated, lowercase format.
    """
    if isinstance(mac, bytes):
        mac = mac.decode()
    if ":" not in mac and len(mac) == 12:
        mac = ":".join(mac[i:i+2] for i in range(0, 12, 2))
    return mac.lower()

def get_vendor_online(mac):
    """
    Looks up vendor information online using the macvendors.com API.
    Uses a simple User-Agent header generated via ua_generator.
    Returns the vendor name if found, otherwise "Unknown".
    """
    try:
        mac = format_mac(mac)
        url = f"https://api.macvendors.com/{mac}"
        # Generate a robust User-Agent header.
        ua = ua_generator.generate(device="desktop", browser="chrome")
        headers = ua.headers.get()
        # Fallback to a simple UA if needed.
        if "User-Agent" not in headers:
            headers["User-Agent"] = "Mozilla/5.0"
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200 and response.text and "not found" not in response.text.lower():
            return response.text.strip()
        return "Unknown"
    except Exception as e:
        print(f"Lookup error for {mac}: {e}")
        return "Unknown"

def get_vendor_info(mac):
    """
    Retrieves vendor information for the given MAC address.
    Checks the local cache first; if not found, performs an online lookup,
    caches the result, and returns the vendor name.
    """
    mac = format_mac(mac)
    if mac in known_devices:
        return known_devices[mac]
    vendor = get_vendor_online(mac)
    cache_vendor(mac, vendor)
    known_devices[mac] = vendor
    return vendor

def get_vendor_info_wrapper(mac):
    """
    Wrapper for get_vendor_info() that returns "Unknown" if an error occurs.
    """
    try:
        return get_vendor_info(mac)
    except Exception:
        return "Unknown"

def scan_network(network, interface):
    """
    Performs an ARP scan on the specified network.
    Returns a list of dictionaries for each discovered device with keys: 'ip', 'mac', 'vendor'.
    Ensures that the scanning device (local host) is included.
    """
    arp_request = ARP(pdst=network)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request
    answered_list = srp(packet, timeout=3, verbose=0)[0]
    devices = []
    for sent, received in answered_list:
        vendor = get_vendor_info_wrapper(received.hwsrc)
        devices.append({"ip": received.psrc, "mac": received.hwsrc, "vendor": vendor})
    # Include local device if not found.
    local_ip = get_if_addr(interface)
    local_mac = get_if_hwaddr(interface)
    if not any(d["ip"] == local_ip for d in devices):
        local_vendor = get_vendor_info_wrapper(local_mac)
        devices.append({"ip": local_ip, "mac": local_mac, "vendor": local_vendor})
    return devices

def display_devices(devices, local_ip, local_hostname):
    """
    Formats the scan results into a table.
    If the local device's vendor is "Unknown", the hostname is appended.
    """
    table = []
    for device in devices:
        vendor = device["vendor"]
        if device["ip"] == local_ip and vendor == "Unknown":
            vendor = f"Unknown ({local_hostname})"
        table.append([device["ip"], device["mac"], vendor])
    return tabulate(
        table,
        headers=[
            f"{Fore.GREEN}IP Address{Fore.RESET}",
            f"{Fore.RED}MAC Address{Fore.RESET}",
            f"{Fore.LIGHTWHITE_EX}Vendor{Fore.RESET}",
        ],
        tablefmt="heavy_grid",
    )

def perform_scan():
    """
    Detects the default interface, computes the network range, and performs an ARP scan.
    Displays a progress bar while scanning.
    Returns a tuple: (devices, local_ip, local_hostname).
    """
    interface = get_default_interface()
    if not interface:
        raise Exception("Could not detect a default network interface.")
    network_range = get_network_range(interface)
    if not network_range:
        raise Exception("Could not determine the network range. Please check your interface settings.")
    devices = []
    def scan_job():
        nonlocal devices
        devices = scan_network(network_range, interface)
    scan_thread = Thread(target=scan_job)
    scan_thread.start()
    total_steps = 100
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.1f}%",
        TimeRemainingColumn(),
        transient=True,
    ) as progress:
        task = progress.add_task("Scanning", total=total_steps)
        for _ in range(total_steps):
            time.sleep(0.075)
            progress.advance(task)
            if not scan_thread.is_alive():
                break
        progress.update(task, completed=total_steps)
    scan_thread.join()
    local_ip = get_if_addr(interface)
    local_hostname = socket.gethostname()
    return devices, local_ip, local_hostname

if __name__ == "__main__":
    ensure_admin()
    try:
        devices, local_ip, local_hostname = perform_scan()
        print(display_devices(devices, local_ip, local_hostname))
    except Exception as e:
        print(f"Error: {e}")
