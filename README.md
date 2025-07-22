# Marstek CT Meter - Home Assistant Integration

<p align="center">
  <img src="https://raw.githubusercontent.com/d-shmt/hass_marstek-smart-meter/main/custom_components/marstek_ct/logo.png" width="150">
</p>

<p align="center">
  A modern, local-polling integration to connect your Marstek CT Smart Meter (CT002/CT003) with Home Assistant.
</p>

<p align="center">
  <a href="https://github.com/d-shmt/hass_marstek-smart-meter/releases"><img src="https://img.shields.io/github/v/release/d-shmt/hass_marstek-smart-meter?style=for-the-badge&color=blue" alt="Latest Release"></a>
  <a href="https://github.com/d-shmt/hass_marstek-smart-meter/issues"><img src="https://img.shields.io/github/issues/d-shmt/hass_marstek-smart-meter?style=for-the-badge&color=orange" alt="Open Issues"></a>
</p>

---

## 🌟 Features

This integration brings your Marstek CT Meter into Home Assistant with a focus on ease of use and local control.

* **💻 UI Configuration:** No YAML needed for setup! Add and configure your meter directly through the Home Assistant user interface.
* **📡 Local Polling:** All data is fetched directly from your device via UDP on your local network. No cloud connection is required.
* **🏠 Automatic Device & Entities:** Creates a device in Home Assistant and automatically adds all relevant sensors.
* **📊 Key Sensors:** Provides sensors for Total Power, Phase A/B/C Power, and WLAN Signal Strength (RSSI).
* **🌐 Multi-Language Support:** The setup process and sensor names will automatically use German if your Home Assistant is set to German, otherwise it defaults to English.

---

## ⚠️ Disclaimer

This is an independent, community-developed integration and is not officially affiliated with or endorsed by **Marstek** or **Hame**. It was created based on publicly available information and community research. Use at your own risk.

---

## 📋 Prerequisites

Before you can install and configure this integration, please ensure you have the following:

* **Hardware:**
    * A supported Marstek CT Smart Meter (e.g., CT002, CT003).
    * A local Wi-Fi network the meter is connected to.

* **Home Assistant:**
    * A working Home Assistant instance.
    * [HACS (Home Assistant Community Store)](https://hacs.xyz/) installed.

* **Information:**
    * The local IP Address of your CT meter.
    * The **Battery MAC** and **CT Meter MAC** addresses. You can find these in the official Marstek mobile app under "Device Management".

---

## 🚀 Installation

Click the buttons below to add this integration to your Home Assistant instance.

### Step 1: Add Repository to HACS

[![Open your Home Assistant instance and add a custom repository][hacs-badge]][hacs-link]

### Step 2: Install the Integration via HACS

After adding the repository, you need to install the integration.

1.  Go to **HACS** > **Integrations**.
2.  Search for **"Marstek CT Meter"** and click on it.
3.  Click the **DOWNLOAD** button and wait for the installation to complete.
4.  **Restart Home Assistant** when prompted.

### Step 3: Configure the Integration

After restarting, you can add and configure the integration.

[![Open your Home Assistant instance and start setting up a new integration.][config-badge]][config-link]

---
[hacs-badge]: https://my.home-assistant.io/badges/hacs_repository.svg
[hacs-link]: https://my.home-assistant.io/redirect/hacs_repository/?owner=d-shmt&repository=hass_marstek-smart-meter&category=integration
[config-badge]: https://my.home-assistant.io/badges/config_flow_start.svg
[config-link]: https://my.home-assistant.io/redirect/config_flow_start/?domain=marstek_ct

---

## 🙏 Acknowledgements

This integration would not have been possible without the foundational work and protocol analysis by R. Weijnen.
* **Original Research:** [rweijnen/marstek-venus-e-firmware-notes](https://github.com/rweijnen/marstek-venus-e-firmware-notes/)

---

## 💬 Feedback & Contributions

If you encounter any issues or have suggestions for improvements, please [**open an issue**](https://github.com/d-shmt/hass_marstek-smart-meter/issues) on this GitHub repository. Contributions are always welcome!
