#!/usr/bin/env python3
import sys
import json
import subprocess
import os
import stat


def check_security():
    """Perform security checks before processing messages"""
    # Check script permissions
    script_path = os.path.abspath(__file__)
    st = os.stat(script_path)

    # Ensure script isn't world-writable
    if bool(st.st_mode & stat.S_IWOTH):
        sys.exit("Error: Script is world-writable")

    # Ensure parent directory isn't world-writable
    parent_dir = os.path.dirname(script_path)
    parent_st = os.stat(parent_dir)
    if bool(parent_st.st_mode & stat.S_IWOTH):
        sys.exit("Error: Parent directory is world-writable")


def validate_message(message):
    """Validate incoming message structure and content"""
    if not isinstance(message, dict):
        raise ValueError("Invalid message format")

    if "link" not in message:
        raise ValueError("Missing required 'link' field")

    link = message["link"]
    if not isinstance(link, str):
        raise ValueError("Link must be a string")

    # Basic URL validation
    if not (
        link.startswith("https://www.youtube.com/")
        or link.startswith("http://www.youtube.com/")
    ):
        raise ValueError("Invalid YouTube URL")

    return link


def read_message():
    """Reads a message from stdin with the native messaging protocol"""
    # Read 4 bytes for message length
    raw_length = sys.stdin.buffer.read(4)
    if len(raw_length) < 4:
        sys.exit(0)

    # Ensure message length is reasonable (e.g., < 1MB)
    message_length = int.from_bytes(raw_length, byteorder="little")
    if message_length > 1024 * 1024:  # 1MB limit
        raise ValueError("Message too large")

    # Read and parse message
    message = sys.stdin.buffer.read(message_length).decode("utf-8")
    return json.loads(message)


def send_message(message):
    """Sends a message to stdout with the native messaging protocol"""
    encoded_message = json.dumps(message).encode("utf-8")
    sys.stdout.buffer.write(len(encoded_message).to_bytes(4, byteorder="little"))
    sys.stdout.buffer.write(encoded_message)
    sys.stdout.buffer.flush()


def launch_clapper(video_link):
    """Safely launch Clapper with the video link"""
    try:
        # Use list form to prevent shell injection
        result = subprocess.run(
            ["flatpak", "run", "com.github.rafostar.Clapper", video_link],
            capture_output=True,
            text=True,
            check=True,
            shell=False,  # Explicitly disable shell
        )
        if result.stderr:
            return True, f"Video sent to Clapper (Note: {result.stderr})"

        return True, "Video sent to Clapper"
    except subprocess.CalledProcessError as e:
        return False, f"Clapper error: {e.stderr}"
    except subprocess.SubprocessError as e:
        return False, f"Failed to launch Clapper: {str(e)}"


def main():
    try:
        # Perform security checks
        check_security()

        # Read and validate message
        message = read_message()
        video_link = validate_message(message)

        # Launch Clapper
        success, msg = launch_clapper(video_link)
        send_message({"success": success, "message": msg})

    except Exception as e:
        send_message({"success": False, "error": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
