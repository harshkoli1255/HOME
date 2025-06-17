#!/opt/homebrew/bin/python3.10
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from tabulate import tabulate
# from webdriver_manager.chrome import ChromeDriverManager 
# from selenium.webdriver.chrome.service import Service
import subprocess
import credentials
import re
import time
import platform
import os
from rich.progress import Progress
from colorama import init, Fore,Style
from tabulate import tabulate
from scan import perform_scan, display_devices, load_known_devices
from dotenv import load_dotenv

init()
url1 = "http://192.168.29.1/"
# url2 = "http://10.59.201.44/"

def jioOptions():
    # Define the header and options
    header = [f"{Fore.LIGHTRED_EX}{Style.BRIGHT}Choose An Option{Fore.RESET}", f"{Fore.LIGHTRED_EX}{Style.BRIGHT}Description{Fore.RESET}"]
    options = [
        [f"{Fore.GREEN}1 | login{Fore.RESET}", f"{Fore.CYAN}{Style.BRIGHT}login to the 192.168.29.1 Dashboard{Fore.RESET}"],
        [f"{Fore.GREEN}2 | logout{Fore.RESET}", f"{Fore.CYAN}{Style.BRIGHT}logout{Fore.RESET}"],
        [f"{Fore.GREEN}3 | reboot{Fore.RESET}", f"{Fore.CYAN}{Style.BRIGHT}Reboot Router{Fore.RESET}"],
        [f"{Fore.GREEN}4{Fore.RESET}", f"{Fore.CYAN}{Style.BRIGHT}View LAN IPv4 Reserved IPs Devices{Fore.RESET}"],
        [f"{Fore.GREEN}5{Fore.RESET}", f"{Fore.CYAN}{Style.BRIGHT}LAN IPv4 Reserved IPs Devices{Fore.RESET}"],
        [f"{Fore.GREEN}6{Fore.RESET}", f"{Fore.CYAN}{Style.BRIGHT}Delete LAN IPv4 Reserved IPs Devices{Fore.RESET}"],
        [f"{Fore.GREEN}7{Fore.RESET}", f"{Fore.CYAN}{Style.BRIGHT}MAC Filter Devices{Fore.RESET}"],
        [f"{Fore.GREEN}8{Fore.RESET}", f"{Fore.CYAN}{Style.BRIGHT}View MAC Filter Devices{Fore.RESET}"],
        [f"{Fore.GREEN}9{Fore.RESET}", f"{Fore.CYAN}{Style.BRIGHT}Delete MAC Filter Devices{Fore.RESET}"],
        [f"{Fore.GREEN}10{Fore.RESET}", f"{Fore.CYAN}{Style.BRIGHT}View Connected Clients{Fore.RESET}"],
        [f"{Fore.GREEN}scan{Fore.RESET}", f"{Fore.CYAN}{Style.BRIGHT}Scan Devices On The Network{Fore.RESET}"],
        [f"{Fore.GREEN}exit{Fore.RESET}", f"{Fore.CYAN}{Style.BRIGHT}Exit{Fore.RESET}"],
        [f"{Fore.GREEN}clear{Fore.RESET}", f"{Fore.CYAN}{Style.BRIGHT}Clear Screen{Fore.RESET}"],
        [f"{Fore.GREEN}options{Fore.RESET}", f"{Fore.CYAN}{Style.BRIGHT}Show All Options{Fore.RESET}"],
        [f"{Fore.GREEN}back{Fore.RESET}", f"{Fore.CYAN}{Style.BRIGHT}Back From The Selected Option{Fore.RESET}"],
    ]
    # print(tabulate(options, headers=header, tablefmt="fancy_grid"))
    print(tabulate(options,headers=header, tablefmt="heavy_grid"))

# Function to get input with history support
def input_with_history(prompt):
    return input(prompt)

def tableData(title):
    print(tabulate([[Fore.LIGHTYELLOW_EX+Style.BRIGHT+title+Fore.RESET]], tablefmt="fancy_grid"))
    # Assuming 'table' is already defined and populated as per your original code
    table = wait.until(EC.visibility_of_element_located((By.ID, "recordsData")))
    headers = [Fore.LIGHTRED_EX+Style.BRIGHT+header.text+Fore.RESET for header in table.find_elements(By.TAG_NAME, 'th')]
    rows = table.find_elements(By.TAG_NAME, 'tr')
    data = []  # List to hold all row data
    for row in rows:
        # Extract cells in each row
        cells = row.find_elements(By.TAG_NAME, 'td')
        # Get text from each cell and store it in a list
        row_data = [Fore.GREEN+Style.BRIGHT+cell.text+Fore.RESET for cell in cells]
        if row_data:  # Check if row_data is not empty
            data.append(row_data)  # Add the row data to the list

    # Print all data rows using tabulate
    if data:  # Only print if there is data
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
    else:
        print("No data available.")

def format_mac_address(mac):
    # Remove any existing separators (colons or hyphens)
    mac = mac.replace(':', '').replace('-', '')

    # Check if the input is a valid 12-character hex string
    if len(mac) == 12 and all(c in '0123456789ABCDEFabcdef' for c in mac):
        # Format the MAC address with colons
        formatted_mac = ':'.join(mac[i:i + 2] for i in range(0, 12, 2))
        return formatted_mac

    return None  # Return None if the MAC address is invalid

def is_valid_mac_address(mac):
    # Regular expression pattern for validating MAC address
    pattern = r'^([0-9A-Fa-f]{2}(:|[-])?){5}([0-9A-Fa-f]{2})$'
    
    # Use re.match to check if the MAC address matches the pattern
    return bool(re.match(pattern, mac))

def is_valid_ip(ip_address):
    # Define the regex pattern for the specific IP format
    pattern = r'^192\.168\.29\.(\d{1,3})$'
    
    # Match the IP address against the pattern
    match = re.match(pattern, ip_address)
    
    if match:
        # Extract the last octet and check if it's a valid number between 0-255
        last_octet = int(match.group(1))
        if 0 <= last_octet <= 255:
            return True
    return False

def openPage():
    driver.get(url1)
    try:
        errorMessage = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "msgError"))).get_property("innerText")
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] 192.168.29.1 Responding: {Fore.LIGHTWHITE_EX}{Style.BRIGHT}{errorMessage}{Fore.RESET}")
    except Exception:
        pass

def login():
    try:
        load_dotenv()
        username_field = wait.until(EC.visibility_of_element_located((By.ID, "tf1_userName")))
        username_field.clear()
        # username_field.send_keys(credentials.username)
        username_field.send_keys(os.getenv("username"))
        password_field = wait.until(EC.visibility_of_element_located((By.ID, "tf1_password")))
        password_field.clear()
        # password_field.send_keys(credentials.password)
        password_field.send_keys(os.getenv("password"))
        
        wait.until(EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Login']"))).click()
        try:
            Configuration_Manager = wait.until(EC.visibility_of_element_located((By.XPATH, "//form[@id='tf1_forcedLoginForm']//span[text()=\"An Active Session already exists for the User 'admin'.\"]")))
            Configuration_Manager_TEXT = Configuration_Manager.get_property("innerText")
            
            if("An Active Session already exists for the User" in Configuration_Manager_TEXT):
                driver.execute_script("continueValidate();")

        except Exception:
            while True:
                try:
                    errorMessage = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "msgError"))).get_property("innerText")

                    if("LOGIN_INVALID_CREDENTIALS" or len(errorMessage)!=0 in errorMessage):
                        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] 192.168.29.1 Responding: {Fore.LIGHTWHITE_EX}{Style.BRIGHT}{errorMessage}{Fore.RESET}")
                        login()
                    else:
                        break
                except Exception:
                    break
    except Exception:
        # if(logout(if_is_logout=False)):
        #     login_username = wait.until(EC.visibility_of_element_located((By.ID, "lblLoggedinUser")))
        #     current_loggedin_username  = login_username.text.replace("Hi, ", "")
        #     # print(f"[+] you already logged in as {current_loggedin_username}")
        #     return current_loggedin_username
        pass

def logout():
    driver.execute_script("closeConfirmForm();")
    driver.get("http://192.168.29.1/platform.cgi?page=index.html")

def restart():
    driver.execute_script("gotoLinks('factoryDefault.html');")
    try:
        unAuthorisedMsg = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "unAuthorised"))).text
        print(f"{Fore.LIGHTRED_EX}[-] {unAuthorisedMsg}{Style.BRIGHT}{Fore.RESET}")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Click here to Relogin']"))).click()
        login()
        driver.execute_script("gotoLinks('factoryDefault.html');")

    except Exception:
        try:
            login()
            driver.execute_script("gotoLinks('factoryDefault.html');")
        except Exception:
            driver.execute_script("gotoLinks('factoryDefault.html');")

    # driver.execute_script("backupRestoreRebootTwo();")
    wait.until(EC.visibility_of_element_located((By.NAME, "button.reboot.statusPage"))).click()
    confirmAlert = driver.switch_to.alert
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] {confirmAlert.text}{Fore.RESET}")
    time.sleep(1)
    confirmAlert.accept()

    while True:
        try:
            restartingStatus = wait.until(EC.visibility_of_element_located((By.ID, "lblStatusMsg"))).text
            print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] {restartingStatus}{Fore.RESET}")
        except Exception:
            break

def lanIPV4Configuration():
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[normalize-space()='LAN IPv4 Reserved IPs']")))
        Select(driver.find_element(By.NAME, "recordsData_length")).select_by_value("100")
        titleOfThePage =  wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        tableData(title=titleOfThePage)

    except Exception:
        driver.execute_script("gotoLinks('lanIPv4Config.html');")
        driver.execute_script("gotoLinks('lanIPv4ReservedIPs.html');")
        try:
            unAuthorisedMsg = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "unAuthorised"))).text
            print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {unAuthorisedMsg}{Fore.RESET}")
            wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Click here to Relogin']"))).click()
            login()
            driver.execute_script("gotoLinks('lanIPv4Config.html');")
            driver.execute_script("gotoLinks('lanIPv4ReservedIPs.html');")
        except Exception:
            try:
                login()
                driver.execute_script("gotoLinks('lanIPv4ReservedIPs.html');")
            except Exception:
                driver.execute_script("gotoLinks('lanIPv4ReservedIPs.html');")

        Select(driver.find_element(By.NAME, "recordsData_length")).select_by_value("100")
        titleOfThePage =  wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        tableData(title=titleOfThePage)

def addLanIpv4ResevedIps():
    driver.execute_script("gotoLinks('lanIPv4Config.html');")
    driver.execute_script("gotoLinks('lanIPv4ReservedIPs.html');")
    try:
        unAuthorisedMsg = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "unAuthorised"))).text
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {unAuthorisedMsg}{Fore.RESET}")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Click here to Relogin']"))).click()
        login()
        driver.execute_script("gotoLinks('lanIPv4Config.html');")
        driver.execute_script("gotoLinks('lanIPv4ReservedIPs.html');")
    except Exception:
        try:
            login()
            driver.execute_script("gotoLinks('lanIPv4ReservedIPs.html');")
        except Exception:
            driver.execute_script("gotoLinks('lanIPv4ReservedIPs.html');")

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btnAddNew"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "tf1_hostName"))).send_keys(deviceName)
    wait.until(EC.visibility_of_element_located((By.ID, "tf1_ipAddr"))).send_keys(ipAddress)
    wait.until(EC.visibility_of_element_located((By.ID, "tf1_macAddr"))).send_keys(format_mac_address((deviceMacAddress)))
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btnSubmit"))).click()
    try:
        isalrt = driver.switch_to.alert
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {isalrt.text}{Fore.RESET}")
        isalrt.accept()
    except Exception:
        try:
            msgInfo = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "msgInfo"))).text
            if("succeeded" in msgInfo):
                print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] {msgInfo}{Fore.RESET}")
            else:
                print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {msgInfo}{Fore.RESET}")
        except Exception:
            pass

def deletelanIPV4ConfigurationDevices(deviceMacAddress):

    driver.execute_script("gotoLinks('lanIPv4Config.html');")
    driver.execute_script("gotoLinks('lanIPv4ReservedIPs.html');")
    try:
        unAuthorisedMsg = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "unAuthorised"))).text
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {unAuthorisedMsg}{Fore.RESET}")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Click here to Relogin']"))).click()
        login()
        driver.execute_script("gotoLinks('lanIPv4Config.html');")
        driver.execute_script("gotoLinks('lanIPv4ReservedIPs.html');")
    except Exception:
        try:
            login()
            driver.execute_script("gotoLinks('lanIPv4ReservedIPs.html');")
        except Exception:
            driver.execute_script("gotoLinks('lanIPv4ReservedIPs.html');")

    Select(driver.find_element(By.NAME, "recordsData_length")).select_by_value("100")
    achains = ActionChains(driver)
    try:
        mac_address_cell = driver.find_element(By.XPATH, f"//td[contains(text(), '{format_mac_address(deviceMacAddress)}')]")
        achains.context_click(mac_address_cell).perform()
        wait.until(EC.visibility_of_element_located((By.ID, "deleteMenu"))).click()
    except Exception:
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] MAC Address You Enter {Fore.RESET}{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}'{format_mac_address(deviceMacAddress)}'{Fore.RESET}{Fore.LIGHTRED_EX}{Style.BRIGHT} is Not Present In The LAN IPv4 Reserved IPs{Fore.RESET}")
    try:
        msgInfo = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "msgInfo"))).text
        if("succeeded" in msgInfo):
            print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] {msgInfo}{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {msgInfo}{Fore.RESET}")
    except Exception:
        pass

def macFilter():
    driver.execute_script("gotoLinks('accessPoints.html');")
    try:
        unAuthorisedMsg = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "unAuthorised"))).text
        print(f"{Fore.LIGHTRED_EX}[-] {unAuthorisedMsg}{Style.BRIGHT}{Fore.RESET}")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Click here to Relogin']"))).click()
        login()
        driver.execute_script("gotoLinks('accessPoints.html');")
    except Exception:
        try:
            login()
            driver.execute_script("gotoLinks('accessPoints.html');")
        except Exception:
            driver.execute_script("gotoLinks('accessPoints.html');")

    achains = ActionChains(driver)
    # JioFiber
    JioFibreSSID = wait.until(EC.visibility_of_element_located((By.XPATH, "//td[normalize-space()='JioFibre']")))
    achains.context_click(JioFibreSSID).perform()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@id='macFilterMenu']"))).click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btnAddNew"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "txtMacAddr"))).send_keys(format_mac_address((deviceMacAddress)))
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btnSubmit"))).click()

    try:
        isAlert = driver.switch_to.alert
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {isAlert.text}{Fore.RESET}")
        isAlert.accept()
    except Exception:
        # JioFiber5G
        driver.execute_script("gotoLinks('accessPoints.html');")
        JioFiber5GSSID = wait.until(EC.visibility_of_element_located((By.XPATH, "//td[normalize-space()='JioFiber5G']")))
        achains.context_click(JioFiber5GSSID).perform()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@id='macFilterMenu']"))).click()
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btnAddNew"))).click()
        wait.until(EC.visibility_of_element_located((By.ID, "txtMacAddr"))).send_keys(format_mac_address((deviceMacAddress)))
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btnSubmit"))).click()
        
        try:
            msgInfo = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "msgInfo"))).text
            if("succeeded" in msgInfo):
                print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] {msgInfo}{Fore.RESET}")
            else:
                print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {msgInfo}{Fore.RESET}")
        except Exception:
            pass

def deleteMacFilterDevices(deviceMacAddress):
    driver.execute_script("gotoLinks('accessPoints.html');")
    try:
        unAuthorisedMsg = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "unAuthorised"))).text
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {unAuthorisedMsg}{Fore.RESET}")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Click here to Relogin']"))).click()
        login()
        driver.execute_script("gotoLinks('accessPoints.html');")
    except Exception:
        try:
            login()
            driver.execute_script("gotoLinks('accessPoints.html');")
        except Exception:
            driver.execute_script("gotoLinks('accessPoints.html');")

    achains = ActionChains(driver)
    # JioFiber
    JioFibreSSID = wait.until(EC.visibility_of_element_located((By.XPATH, "//td[normalize-space()='JioFibre']")))
    achains.context_click(JioFibreSSID).perform()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@id='macFilterMenu']"))).click()

    Select(driver.find_element(By.NAME, "recordsData_length")).select_by_value("100")
    try:
        mac_address_cell = driver.find_element(By.XPATH, f"//td[contains(text(), '{format_mac_address((deviceMacAddress))}')]")
        achains.context_click(mac_address_cell).perform()
        wait.until(EC.visibility_of_element_located((By.ID, "deleteMenu"))).click()
    except Exception:
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] MAC Address You Enter {Fore.RESET}{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}'{formatted_mac}'{Fore.RESET}{Fore.LIGHTRED_EX}{Style.BRIGHT} is Not Present In The JioFiber")

    # JioFiber5G
    driver.execute_script("gotoLinks('accessPoints.html');")
    JioFiber5GSSID = wait.until(EC.visibility_of_element_located((By.XPATH, "//td[normalize-space()='JioFiber5G']")))
    achains.context_click(JioFiber5GSSID).perform()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@id='macFilterMenu']"))).click()

    Select(driver.find_element(By.NAME, "recordsData_length")).select_by_value("100")
    try:
        mac_address_cell = driver.find_element(By.XPATH, f"//td[contains(text(), '{format_mac_address((deviceMacAddress))}')]")
        achains.context_click(mac_address_cell).perform()
        wait.until(EC.visibility_of_element_located((By.ID, "deleteMenu"))).click()
    except Exception:
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] MAC Address You Enter {Fore.RESET}{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}'{formatted_mac}'{Fore.RESET}{Fore.LIGHTRED_EX}{Style.BRIGHT} is Not Present In The JioFiber5G")

    try:
        msgInfo = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "msgInfo"))).text
        if("succeeded" in msgInfo):
            print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] {msgInfo}{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {msgInfo}{Fore.RESET}")
    except Exception:
        pass

def listMacFilterDevices():
    try:
        driver.execute_script("gotoLinks('accessPoints.html');")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[normalize-space()='MAC Filter']")))
        Select(driver.find_element(By.NAME, "recordsData_length")).select_by_value("100")
        # Assuming 'table' is already defined and populated as per your original code
        titleOfThePage =  wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        tableData(title=f"JioFiber {titleOfThePage}")
    except Exception:
        driver.execute_script("gotoLinks('accessPoints.html');")
        try:
            unAuthorisedMsg = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "unAuthorised"))).text
            print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {unAuthorisedMsg}{Fore.RESET}")
            wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Click here to Relogin']"))).click()
            login()
            driver.execute_script("gotoLinks('accessPoints.html');")
        except Exception:
            try:
                login()
                driver.execute_script("gotoLinks('accessPoints.html');")
            except Exception:
                driver.execute_script("gotoLinks('accessPoints.html');")

        achains = ActionChains(driver)
        # JioFiber
        JioFibreSSID = wait.until(EC.visibility_of_element_located((By.XPATH, "//td[normalize-space()='JioFibre']")))
        achains.context_click(JioFibreSSID).perform()
        # wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@id='macFilterMenu']"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@id='macFilterMenu']"))).click()

        Select(driver.find_element(By.NAME, "recordsData_length")).select_by_value("100")
        # Assuming 'table' is already defined and populated as per your original code
        titleOfThePage =  wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        tableData(title=f"JioFiber {titleOfThePage}")

    # JioFiber5G
    try:
        driver.execute_script("gotoLinks('accessPoints.html');")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[normalize-space()='MAC Filter']")))
        Select(driver.find_element(By.NAME, "recordsData_length")).select_by_value("100")
        # Assuming 'table' is already defined and populated as per your original code
        titleOfThePage =  wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        tableData(title=f"JioFiber5G {titleOfThePage}")

    except Exception:
        driver.execute_script("gotoLinks('accessPoints.html');")
        JioFiber5GSSID = wait.until(EC.visibility_of_element_located((By.XPATH, "//td[normalize-space()='JioFiber5G']")))
        achains.context_click(JioFiber5GSSID).perform()
        # wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@id='macFilterMenu']"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@id='macFilterMenu']"))).click()

        Select(driver.find_element(By.NAME, "recordsData_length")).select_by_value("100")
        # Assuming 'table' is already defined and populated as per your original code
        titleOfThePage =  wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        tableData(title=f"JioFiber5G {titleOfThePage}")

def connectedClients():
    try:
        driver.execute_script("gotoLinks('accessPoints.html');")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[normalize-space()='Connected Clients']")))
        Select(driver.find_element(By.NAME, "recordsData_length")).select_by_value("100")
        titleOfThePage =  wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        tableData(title=f"JioFiber {titleOfThePage}")

    except Exception:
        driver.execute_script("gotoLinks('accessPoints.html');")
        try:
            unAuthorisedMsg = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "unAuthorised"))).text
            print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {unAuthorisedMsg}{Fore.RESET}")
            wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Click here to Relogin']"))).click()
            login()
            driver.execute_script("gotoLinks('accessPoints.html');")
        except Exception:
            try:
                login()
                driver.execute_script("gotoLinks('accessPoints.html');")
            except Exception:
                driver.execute_script("gotoLinks('accessPoints.html');")

        achains = ActionChains(driver)
        # JioFiber
        JioFibreSSID = wait.until(EC.visibility_of_element_located((By.XPATH, "//td[normalize-space()='JioFibre']")))
        achains.context_click(JioFibreSSID).perform()
        wait.until(EC.visibility_of_element_located((By.XPATH,"//li[@id='statusMenu']"))).click()

        Select(driver.find_element(By.NAME, "recordsData_length")).select_by_value("100")
        titleOfThePage =  wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        tableData(title=f"JioFiber {titleOfThePage}")

    # JioFiber5G
    try:
        driver.execute_script("gotoLinks('accessPoints.html');")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[normalize-space()='Connected Clients']")))
        Select(driver.find_element(By.NAME, "recordsData_length")).select_by_value("100")
        titleOfThePage =  wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        tableData(title=f"JioFiber5G {titleOfThePage}")

    except Exception:
        driver.execute_script("gotoLinks('accessPoints.html');")
        JioFiber5GSSID = wait.until(EC.visibility_of_element_located((By.XPATH, "//td[normalize-space()='JioFiber5G']")))
        achains.context_click(JioFiber5GSSID).perform()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@id='statusMenu']"))).click()

        Select(driver.find_element(By.NAME, "recordsData_length")).select_by_value("100")
        titleOfThePage =  wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        tableData(title=f"JioFiber5G {titleOfThePage}")

def init_driver(headless=False):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    if headless:
        chrome_options.add_argument("--headless")
        # You might also want to add additional flags depending on your setup:
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--window-size=1920,1080")
    # service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 2)
    return driver, wait

# Print the full platform information
platformInformation = platform.platform().lower()
jioOptions()
islogout = None

while True:
    try:
        option = input_with_history(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}>>>{Fore.RESET}{Fore.LIGHTWHITE_EX}{Style.BRIGHT} (Select Option): {Fore.RESET}").lower()
        if("clear" in option):
            if("windows" in platformInformation):
                os.system("cls")
            else:
                subprocess.call("clear")

        elif("scan" in option):
            # with Progress() as progress:
            #     _ = progress.add_task("",total=None)
            known_devices = load_known_devices()
            try:
                devices, local_ip, local_hostname = perform_scan()
                # print("Devices on the network:")
                print(display_devices(devices, local_ip, local_hostname))
            except Exception as e:
                print(f"Error during network scan: {e}")

        elif("option" in option or "help" in option):
            # subprocess.call("clear")
            jioOptions()
    
    except Exception:
        continue

    if(option=="1" or "login" in option):
        with Progress() as progress:
            _ = progress.add_task("",total=None)  
            while True:
                try:
                    logged_in_username = login()
                    while True:
                        login_username = wait.until(EC.visibility_of_element_located((By.ID, "lblLoggedinUser"))).text
                        if("Hi" in login_username):
                            current_loggedin_username  = login_username.replace("Hi, ", "")
                            if(islogout==False):
                                print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] you now logged in as {Fore.RESET}{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}{current_loggedin_username}{Fore.RESET}")
                                islogout=True
                            elif(islogout==True or islogout==None):
                                print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] you already logged in as {Fore.RESET}{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}{current_loggedin_username}{Fore.RESET}")
                                islogout = None
                            break
                        else:
                            dashboard = wait.until(EC.visibility_of_element_located((By.ID, "mainMenu1")))
                            dashboard.click()
                            continue

                except Exception as e:
                    driver, wait = init_driver(headless=False)
                    openPage()
                    login()
                    while True:
                        login_username = wait.until(EC.visibility_of_element_located((By.ID, "lblLoggedinUser"))).text
                        if("Hi" in login_username):
                            current_loggedin_username  = login_username.replace("Hi, ", "")
                            print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] you now logged in as {Fore.RESET}{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}{current_loggedin_username}{Fore.RESET}")
                            break
                        else:
                            dashboard = wait.until(EC.visibility_of_element_located((By.ID, "mainMenu1")))
                            dashboard.click()
                            continue
                break
    
    elif(option=="2" or (" " and "2") in option or "logout" in option):
        with Progress() as progress:
            _ = progress.add_task("",total=None)  
            while True:        
                try:
                    login_username = wait.until(EC.visibility_of_element_located((By.ID, "lblLoggedinUser")))
                    logout()
                    islogout = False
                    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] logout successfully{Fore.RESET}")
                except Exception:
                    print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] It looks like you're not logged in right now{Fore.RESET}")
                break
        
    elif(option=="3"  or "reboot" in option or ((" " and "3") in option)):
        while True:
            rebootPermission = input_with_history(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[^_^] Comfirm Reboot (y/n): {Fore.RESET}").lower()
            try:
                if(rebootPermission=="y" or "yes" in rebootPermission):
                    with Progress() as progress:
                        _ = progress.add_task("",total=None) 
                        try:
                            restart()
                        except Exception:
                            try:
                                login()
                                restart()
                                print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] Restarted Successfully{Fore.RESET}")
                            except Exception:
                                driver, wait = init_driver(headless=False)
                                openPage()
                                login()
                                restart()
                                print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] Restarted Successfully{Fore.RESET}")
                                break
                elif(rebootPermission=="n" or "no" in rebootPermission or "back" in rebootPermission or "exit" in rebootPermission):
                    break
            except Exception:
                continue

    elif (option=="4" or ((" " and "4") in option)):
        with Progress() as progress:
            _ = progress.add_task("",total=None)  
            while True:  
                try:
                    lanIPV4Configuration()
                except Exception:
                    try:
                        login()
                        lanIPV4Configuration()
                    except Exception:
                        driver, wait = init_driver(headless=False)
                        openPage()
                        login()
                        lanIPV4Configuration()
                break
                
    elif(option=="5" or (" " and "5") in option):
        deviceName = input_with_history(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}[{option}] Enter Device Name: {Fore.RESET}")
        if("back" in deviceName or "exit" in deviceName):
            continue
        while True:
            ipAddress = input_with_history(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}[{option}] Enter Device IP Address: {Fore.RESET}")
            if("back" in ipAddress or "exit" in ipAddress):
                break
            if is_valid_ip(ipAddress):
                # Flag to indicate completion of inner loop
                inner_loop_completed = False
                while True:
                    deviceMacAddress = input_with_history(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}[{option}] Enter Device MAC Address: {Fore.RESET}")
                    if("back" in deviceMacAddress or "exit" in deviceMacAddress):
                        break
                    try:
                        formatted_mac = format_mac_address(deviceMacAddress)
                        if is_valid_mac_address(formatted_mac):
                            with Progress() as progress:
                                _ = progress.add_task("",total=None) 
                                try:
                                    addLanIpv4ResevedIps()
                                    inner_loop_completed = True  # Mark inner loop as completed
                                except Exception:
                                    try:
                                        login()
                                        addLanIpv4ResevedIps()
                                        inner_loop_completed = True  # Mark inner loop as completed
                                    except Exception:
                                        driver, wait = init_driver(headless=False)
                                        openPage()
                                        login()
                                        addLanIpv4ResevedIps()
                                        inner_loop_completed = True  # Mark inner loop as completed
                                
                                # Break the inner loop if completed successfully
                                if inner_loop_completed:
                                    break
                    except Exception:
                        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {Fore.RESET}{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}'{deviceMacAddress}'{Fore.RESET}{Fore.LIGHTRED_EX}{Style.BRIGHT} You Enter is not a valid MAC address.{Fore.RESET}")
                        continue
                # Break the outer loop if the inner loop completed successfully
                break
            else:
                print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {Fore.RESET}{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}'{ipAddress}'{Fore.RESET}{Fore.LIGHTRED_EX}{Style.BRIGHT} You Enter is not a valid IP address.{Fore.RESET}")

    elif(option=="6" or (" " and "6") in option):
        # macAddressFilter = "8E:82:70:F6:3C:92"
        while True:
            deviceMacAddress = input_with_history(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}[{option}] Enter Device MAC Address: {Fore.RESET}")
            if("back" in deviceMacAddress or "exit" in deviceMacAddress):
                break
            try:
                formatted_mac = format_mac_address((deviceMacAddress))
                if is_valid_mac_address(formatted_mac):
                    with Progress() as progress:
                        _ = progress.add_task("",total=None) 
                        try:
                            deletelanIPV4ConfigurationDevices(deviceMacAddress=formatted_mac)
                        except Exception:
                            try:
                                login()
                                deletelanIPV4ConfigurationDevices(deviceMacAddress=formatted_mac)
                            except Exception:
                                driver, wait = init_driver(headless=False)
                                openPage()
                                login()
                                deletelanIPV4ConfigurationDevices(deviceMacAddress=formatted_mac)
            except Exception:
                print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {Fore.RESET}{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}'{deviceMacAddress}'{Fore.RESET}{Fore.LIGHTRED_EX}{Style.BRIGHT} You Enter is not a valid MAC address.{Fore.RESET}")
                continue
            break


    elif(option=="7" or ((" " and "7") in option)):
        # macAddressFilter = "8E:82:70:F6:3C:92"
        while True:
            deviceMacAddress = input_with_history(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[{option}] Enter Device Mac Address: {Fore.RESET}")
            if("back" in deviceMacAddress or "exit" in deviceMacAddress):
                break
            try:
                formatted_mac = format_mac_address((deviceMacAddress))
                if is_valid_mac_address(formatted_mac):
                    with Progress() as progress:
                        _ = progress.add_task("",total=None) 
                        try:
                            macFilter()
                        except Exception:
                            try:
                                login()
                                macFilter()
                            except Exception:
                                driver, wait = init_driver(headless=False)
                                openPage()
                                login()
                                macFilter()
                        break
            except Exception:
                print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {Fore.RESET}{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}'{deviceMacAddress}'{Fore.RESET}{Fore.LIGHTRED_EX}{Style.BRIGHT} You Enter is not a valid MAC address.{Fore.RESET}")
                continue

    elif (option=="8" or ((" " and "8") in option)):
        with Progress() as progress:
            # _ = progress.add_task("Loading...", total=None)  
            _ = progress.add_task("",total=None)  
            while True:
                try:
                    listMacFilterDevices()
                except Exception:
                    try:
                        login()
                        listMacFilterDevices()
                    except Exception:
                        driver, wait = init_driver(headless=False)
                        openPage()
                        login()
                        listMacFilterDevices()
                break
        
    elif (option=="9" or ((" " and "9") in option)):
            while True:
                deviceMacAddress = input_with_history(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[{option}] Enter Device Mac Address:{Fore.RESET} ")
                if("back" in deviceMacAddress or "exit" in deviceMacAddress):
                    break
                try:
                    formatted_mac = format_mac_address((deviceMacAddress))
                    if is_valid_mac_address(formatted_mac):
                        with Progress() as progress:
                            _ = progress.add_task("",total=None) 
                            try:
                                deleteMacFilterDevices(deviceMacAddress=deviceMacAddress)
                            except Exception:
                                try:
                                    login()
                                    deleteMacFilterDevices(deviceMacAddress=deviceMacAddress)
                                except Exception:
                                    driver, wait = init_driver(headless=False)
                                    openPage()
                                    login()
                                    deleteMacFilterDevices(deviceMacAddress=deviceMacAddress)
                except Exception:
                    print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[-] {Fore.RESET}{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}'{deviceMacAddress}'{Fore.RESET}{Fore.LIGHTRED_EX}{Style.BRIGHT} You Enter is not a valid MAC address.{Fore.RESET}")
                    continue
                break

    elif (option=="10" or ((" " and "10") in option)):
        with Progress() as progress:
            _ = progress.add_task("",total=None)  
            while True: 
                try:
                    connectedClients()
                except Exception:
                    try:
                        login()
                        connectedClients()
                    except Exception:
                        driver, wait = init_driver(headless=False)
                        openPage()
                        login()
                        connectedClients()
                break
    elif(option in ("exit","back") or "quit" in option):
        while True:
            quitConfirm = input_with_history((f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[^_^] Are You Sure You Wants To Quit {Fore.RESET}{Fore.LIGHTYELLOW_EX}(Default=yes){Fore.RESET}{Fore.LIGHTGREEN_EX}: {Fore.RESET}")).lower()
            if("y" in quitConfirm or "yes" in quitConfirm or len(quitConfirm)==0):
                try:
                    driver.close()
                    if((platformInformation in ("linux" or "mac"))):
                        try:
                            subprocess.call("/bin/zsh")
                        except Exception:
                            try:
                                subprocess.call("/bin/bash")
                            except Exception:
                                subprocess.call("/bin/sh")
                    elif("windows" in platformInformation):
                        try:
                            os.system('C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe')
                        except Exception:
                            os.system('C:\\Windows\\System32\\cmd.exe')

                except Exception:
                    if((platformInformation in ("linux" or "mac"))):
                        try:
                            subprocess.call("/bin/zsh")
                        except Exception:
                            try:
                                subprocess.call("/bin/bash")
                            except Exception:
                                subprocess.call("/bin/sh")
                    elif("windows" in platformInformation):
                        try:
                            os.system('C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe')
                        except Exception:
                            os.system('C:\\Windows\\System32\\cmd.exe')
                exit()
            elif((quitConfirm in ("n" or "no ")) or ("back" in quitConfirm)):
                break