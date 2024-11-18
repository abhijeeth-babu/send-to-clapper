#!/usr/bin/env python3

import os
import sys
import json

# Define paths relative to the script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOST_DIR = os.path.join(BASE_DIR, "native-messaging-host")
CHROME_MANIFEST_TEMPLATE = os.path.join(HOST_DIR, "chrome", "com.example.clapper.json")
FIREFOX_MANIFEST_TEMPLATE = os.path.join(
    HOST_DIR, "firefox", "com.example.clapper.json"
)
HOST_SCRIPT = os.path.join(HOST_DIR, "clapper_host.py")

FIREFOX_HOST_DIR = os.path.expanduser("~/.mozilla/native-messaging-hosts")
CHROME_HOST_DIR = os.path.expanduser("~/.config/google-chrome/NativeMessagingHosts")
CHROMIUM_HOST_DIR = os.path.expanduser("~/.config/chromium/NativeMessagingHosts")


def ensure_directory_exists(path):
    """Ensure that the target directory exists."""
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        sys.exit(f"Error: Unable to create directory {path}: {e}")


def create_manifest(template_path, output_path):
    """Update the manifest file with the absolute path to the host script."""
    try:
        with open(template_path, "r") as template_file:
            manifest = json.load(template_file)
        manifest["path"] = HOST_SCRIPT
        with open(output_path, "w") as output_file:
            json.dump(manifest, output_file, indent=4)
        print(f"Manifest installed to: {output_path}")
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"Error: Unable to create manifest file: {e}")


def install_for_firefox():
    """Install the native messaging host for Firefox."""
    ensure_directory_exists(FIREFOX_HOST_DIR)
    destination = os.path.join(FIREFOX_HOST_DIR, "com.example.clapper.json")
    create_manifest(FIREFOX_MANIFEST_TEMPLATE, destination)


def install_for_chrome(target_dir):
    """Prepare the native messaging host for Chrome/Chromium."""
    ensure_directory_exists(target_dir)
    destination = os.path.join(target_dir, "com.example.clapper.json")
    create_manifest(CHROME_MANIFEST_TEMPLATE, destination)
    print(
        f"IMPORTANT: Please edit the manifest located at '{destination}' "
        "to replace 'ID' in 'allowed_origins' with your Chrome extension's ID."
    )


def show_manifest(browser):
    """Print the modified manifest file for the specified browser."""
    template_path = (
        FIREFOX_MANIFEST_TEMPLATE if browser == "firefox" else CHROME_MANIFEST_TEMPLATE
    )

    try:
        with open(template_path, "r") as template_file:
            manifest = json.load(template_file)
        manifest["path"] = HOST_SCRIPT
        print(json.dumps(manifest, indent=4))
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"Error: Unable to show {browser} manifest: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: install.py <browser>")
        print("Supported browsers: firefox, chrome, chromium")
        print("Use 'show <browser>' to print the manifest.")
        sys.exit(1)

    action = sys.argv[1].lower()
    if action == "firefox":
        install_for_firefox()
    elif action in ["chrome", "chromium"]:
        target_dir = CHROME_HOST_DIR if action == "chrome" else CHROMIUM_HOST_DIR
        install_for_chrome(target_dir)
    elif action == "show":
        if len(sys.argv) != 3:
            sys.exit("Error: Specify the browser for 'show' (firefox, chrome).")
        browser = sys.argv[2].lower()
        if browser not in ["firefox", "chrome"]:
            sys.exit("Error: Unsupported browser. Use 'firefox' or 'chrome'.")
        show_manifest(browser)
    else:
        sys.exit(
            "Error: Unsupported action. Use 'firefox', 'chrome', 'chromium', or 'show <browser>'."
        )


if __name__ == "__main__":
    main()
