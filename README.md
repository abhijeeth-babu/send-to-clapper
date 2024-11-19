# Send to Clapper  

"Send to Clapper" is a browser extension designed to enhance your video-watching experience by opening YouTube videos and Shorts directly in the [Clapper](https://rafostar.github.io/clapper/) media player. With a single click, the extension pauses the video on YouTube and sends its link to Clapper, allowing you to enjoy smooth playback with Clapper's robust performance and feature set.  

Clapper is a modern and lightweight media player built on top of GStreamer. It’s designed to integrate seamlessly with the GNOME desktop environment, offering excellent support for flatpak apps and the latest media codecs.  

---

## Features  

- **Seamless Playback:** Instantly send YouTube links to Clapper for uninterrupted viewing.  
- **Cross-Browser Support:** Available for Firefox and Chrome/Chromium.  
- **Native Messaging Host:** A secure communication bridge between the extension and Clapper.  

---

## Installation  

### 1. Install the Extension  

#### Firefox  
- Download "Send to Clapper" directly from the [AMO Store](https://addons.mozilla.org/en-US/firefox/addon/send-to-clapper/).  

#### Chrome/Chromium  
- Download the extension from the [GitHub releases](https://github.com/abhijeeth-babu/send-to-clapper/releases).  
- Extract the ZIP file and load the unpacked extension into Chrome/Chromium:  
  1. Go to `chrome://extensions/`.  
  2. Enable **Developer mode**.  
  3. Click **Load unpacked** and select the extracted folder.  

---

### 2. Install the Native Messaging Host  

The native messaging host enables communication between the browser extension and Clapper.  

#### What It Does  
The host script (`clapper_host.py`) receives links from the extension and launches Clapper with the given video URL. It uses a JSON manifest to inform the browser about its location and permissions.  

### Using `installer.py`  

The `installer.py` script sets up the native messaging host for your browser. Clone this repo and run the `installer.py`.  

#### General Usage  
```bash
python3 installer.py <browser>
```

Supported browsers: `firefox`, `chrome`, `chromium`.  

To display the JSON manifest without installation:  
```bash
python3 installer.py show <browser>
```

#### Installation for Firefox  
```bash
python3 installer.py firefox
```
This will:  
1. Copy the manifest file to `~/.mozilla/native-messaging-hosts/`.  
2. Update the manifest with the correct path to `clapper_host.py`.  

#### Installation for Chrome/Chromium  
```bash
python3 installer.py chrome
```
or  
```bash
python3 installer.py chromium
```
This will:  
1. Copy the manifest file to the appropriate location (`~/.config/google-chrome/NativeMessagingHosts/` or `~/.config/chromium/NativeMessagingHosts/`).  
2. **IMPORTANT:** After installation, manually edit the manifest file at the displayed location to replace `ID` in the `allowed_origins` field with your Chrome extension ID (found in `chrome://extensions/`).  

---  

## Tip  

Turn off video previews in the Playback and Performance section of YouTube settings.  

---

## Troubleshooting  

- **Clapper Not Found:** Ensure Clapper is installed via Flatpak. You can install it using:  
  ```bash
  flatpak install flathub com.github.rafostar.Clapper
  ```  
- **Permissions Error:** Ensure the installer script and directories are not world-writable for security reasons.  

---

## Contributing  

Feel free to report issues or submit pull requests to improve the extension or installation process.  

---  

## License  

This project is licensed under the GPLv3. See the [LICENSE](LICENSE) file for details.  

---

Enjoy your seamless video experience with Clapper! 🎥
