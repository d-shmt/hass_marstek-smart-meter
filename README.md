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

## 🚀 Installation

The recommended way to install this integration is through the **Home Assistant Community Store (HACS)**.

1.  **Add Custom Repository in HACS:**
    * In Home Assistant, navigate to `HACS` > `Integrations`.
    * Click the three dots (⋮) in the top right corner and select `Custom repositories`.
    * In the dialog, enter the following:
        * **Repository 🔗:** `https://github.com/d-shmt/hass_marstek-smart-meter`
        * **Category ⚙️:** `Integration`
    * Click **ADD**.

2.  **Install the Integration:**
    * The "Marstek CT Meter" integration will now appear in your HACS list.
    * Click on it and then click **DOWNLOAD**.

3.  **Restart Home Assistant:**
    * After the download is complete, you will be prompted to restart Home Assistant.

---

## 🛠️ Configuration

Once installed, you can add your meter via the UI.

1.  Navigate to **Settings > Devices & Services**.
2.  Click the **+ ADD INTEGRATION** button in the bottom right.
3.  Search for **"Marstek CT Meter"** and select it.
4.  A configuration dialog will appear. Enter the required information:
    * **IP Address:** The local IP address of your CT meter.
    * **MAC Addresses:** The "Battery MAC" and "CT Meter MAC", which can be found in the Marstek mobile app.
5.  Click **SUBMIT**.

The integration will be set up, and a new device with all its sensors will be added to Home Assistant.

---

## 🙏 Acknowledgements

This integration would not have been possible without the foundational work and protocol analysis by R. Weijnen.
* **Original Research:** [rweijnen/marstek-venus-e-firmware-notes](https://github.com/rweijnen/marstek-venus-e-firmware-notes/)

---

## 💬 Feedback & Contributions

If you encounter any issues or have suggestions for improvements, please [**open an issue**](https://github.com/d-shmt/hass_marstek-smart-meter/issues) on this GitHub repository. Contributions are always welcome!
