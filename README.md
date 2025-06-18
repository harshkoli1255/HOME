# 🚀 Jio Fiber CLI Manager

A **cross-platform Python CLI tool** to manage your JioFiber router conveniently from your terminal.<br>
Easily perform **login/logout, manage LAN IPv4 reserved IPs, MAC filtering, view connected clients,** and **scan your local network** directly from your command line.

> **Note:**  
> This tool is for educational and personal use only. Use it responsibly and only on networks you own or have permission to manage.

---

## ✨ Features

- 🔐 **Login/Logout:** Securely authenticate to your JioFiber router's admin dashboard.
- ♻️ **Reboot Router:** Remotely reboot your router from the CLI.
- 📋 **LAN IPv4 Reserved IPs:**
  - View, add, and delete reserved devices.
- 🛡 **MAC Filtering:** Manage, view, and delete MAC filter devices.
- 📶 **Connected Clients:** View all devices currently connected (2.4GHz & 5GHz).
- 🔎 **Network Scan:** Discover all active devices on your local network.
- 🖥 **Terminal Experience:** Clear screen, help/options, and other built-in commands.

---

## ⚡ Quick Start

### 1. **Clone the Repository**

```bash
git clone https://github.com/harshkoli1255/HOME.git
cd HOME
```

### 2. **Set Up a Python Virtual Environment**  
> _Recommended for all platforms to keep dependencies isolated_

#### **Windows**
```powershell
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### **Mac & Linux**
```bash
# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt
```

---

### 3. **Set Environment Variables**

Create a `.env` file in the project root:

```env
username=YOUR_ROUTER_USERNAME
password=YOUR_ROUTER_PASSWORD
```
Replace with your actual JioFiber admin credentials.

---

## 🖥 Usage

> **Do NOT run `jio-fiber.command` directly unless on Mac with matching path.  
> Use the Python CLI as below:**

```bash
python3 main.py
```

You’ll be greeted with a modern, interactive menu:

| Option         | Description                               |
| -------------- | ----------------------------------------- |
| `1` or `login` | Login to the 192.168.29.1 Dashboard       |
| `2` or `logout`| Logout from the router                    |
| `3` or `reboot`| Reboot the router                         |
| `4`            | View LAN IPv4 Reserved IPs Devices        |
| `5`            | Add LAN IPv4 Reserved IPs Devices         |
| `6`            | Delete LAN IPv4 Reserved IPs Devices      |
| `7`            | MAC Filter Devices                        |
| `8`            | View MAC Filter Devices                   |
| `9`            | Delete MAC Filter Devices                 |
| `10`           | View Connected Clients                    |
| `scan`         | Scan Devices On The Network               |
| `clear`        | Clear Screen                              |
| `options`      | Show All Options                          |
| `back`         | Back From The Selected Option             |
| `exit`         | Exit CLI                                  |

Just enter the **option number or command** and follow the prompts.

---

## 🗂 Main Modules

- **`main.py`** — Entry point: CLI, input handler, router automation, menu logic.
- **`scan.py`** — Network scanning, MAC/vendor lookup, device discovery.
- **`requirements.txt`** — All Python dependencies (selenium, tabulate, colorama, rich, scapy, requests, ...).

---

## 🛠 Requirements

- Python **3.7+**
- **Chrome browser** (for Selenium WebDriver automation)
- **ChromeDriver** (managed automatically if using `webdriver-manager`)
- All dependencies from `requirements.txt`

---

## 🛡 Security & Disclaimer

- **Credentials** are read from a `.env` file—**never commit your credentials!**
- This tool automates your browser to interact with the JioFiber admin dashboard.  
  It may break if the dashboard UI changes.
- For **personal/home use only**.  
  Do **not** use on networks you do not own or without explicit permission.

---

## 🐞 Troubleshooting

- **Permissions:** Some functions may require administrator/root privileges.
- **Selenium/ChromeDriver issues:**  
  Ensure your Chrome browser and the `webdriver-manager` package are up-to-date.
- **Network Scan:** Requires `scapy` and may need elevated privileges.

---

## 👨‍💻 Author

Created by [harshkoli1255](https://github.com/harshkoli1255)

---

> **For the most up-to-date and complete feature set, always refer to the actual code and [search the repository on GitHub](https://github.com/harshkoli1255/HOME).**
