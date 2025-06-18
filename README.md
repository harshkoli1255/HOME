# Jio Fiber CLI Manager

A cross-platform Python CLI tool to manage your JioFiber router conveniently from your terminal. Perform login/logout, manage LAN IPv4 reserved IPs, MAC filtering, view connected clients, and scan your network—all from your command line!

**Note:** This tool is for educational and personal use only. Use it responsibly on your own network.

---

## Features

- **Login/Logout:** Authenticate to your JioFiber router's admin dashboard.
- **Reboot Router:** Remotely reboot your router from the CLI.
- **LAN IPv4 Reserved IPs:**
  - View reserved devices
  - Add new reservations
  - Delete devices from reserved list
- **MAC Filtering:**
  - Manage MAC filter devices (add, view, delete)
- **Connected Clients:** View all devices currently connected to your JioFiber router (2.4GHz and 5GHz SSIDs).
- **Network Scan:** Scan your local network to discover active devices.
- **Clear Screen, Help/Options:** Built-in commands for a better terminal experience.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/harshkoli1255/HOME.git
   cd HOME
   ```

2. **Install Python dependencies (preferably in a virtual environment):**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set Environment Variables:**
   Create a `.env` file in the root directory:
   ```
   username=YOUR_ROUTER_USERNAME
   password=YOUR_ROUTER_PASSWORD
   ```
   Replace with your actual JioFiber admin credentials.

---

## Usage

> **Do not run `jio-fiber.command` directly unless on Mac with matching path. Use the Python CLI as below:**

```bash
python3 main.py
```

You’ll be greeted with a menu similar to:

| Option         | Description                               |
| -------------- | ----------------------------------------- |
| 1 \| login     | Login to the 192.168.29.1 Dashboard       |
| 2 \| logout    | Logout from the router                    |
| 3 \| reboot    | Reboot the router                         |
| 4              | View LAN IPv4 Reserved IPs Devices        |
| 5              | Add LAN IPv4 Reserved IPs Devices         |
| 6              | Delete LAN IPv4 Reserved IPs Devices      |
| 7              | MAC Filter Devices                        |
| 8              | View MAC Filter Devices                   |
| 9              | Delete MAC Filter Devices                 |
| 10             | View Connected Clients                    |
| scan           | Scan Devices On The Network               |
| clear          | Clear Screen                              |
| options        | Show All Options                          |
| back           | Back From The Selected Option             |
| exit           | Exit CLI                                  |

Simply enter the desired option (number or command) and follow the prompts.

---

## Main Modules

- **main.py**: The entry point. Handles CLI, user input, router automation, and menu logic.
- **scan.py**: Handles network scanning, MAC/vendor resolution, and device discovery.
- **requirements.txt**: Lists all Python dependencies (selenium, tabulate, colorama, rich, scapy, requests, etc.).

---

## Requirements

- Python 3.7+
- Chrome browser (for Selenium WebDriver automation)
- ChromeDriver (managed automatically if using `webdriver-manager`)
- All dependencies from `requirements.txt`

---

## Security & Disclaimer

- Credentials are read from a `.env` file—**never commit your credentials**.
- This tool automates your browser to interact with the JioFiber admin dashboard. It may break if the dashboard UI changes.
- For **personal/home use only**. Do **not** use on networks you do not own or without permission.

---

## Troubleshooting

- **Permissions:** Some functions may require administrator/root privileges.
- **Selenium/ChromeDriver issues:** Ensure your Chrome browser and the `webdriver-manager` package are up-to-date.
- **Network Scan:** Requires `scapy` and may need elevated privileges.

---

## Author

harshkoli1255

---

## IMPORTANT

This README was generated based on a partial code and file scan. For the most up-to-date and complete feature set, please refer to the actual code and [search the repository on GitHub](https://github.com/harshkoli1255/HOME/search).
