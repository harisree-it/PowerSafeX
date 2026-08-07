
import os
import urllib.request

BLOCKLY_BASE_URL = "https://unpkg.com/blockly/"
FILES = [
    "blockly_compressed.js",
    "blocks_compressed.js",
    "python_compressed.js",
    "msg/js/en.js"
]

TARGET_DIR = "assets/blockly"

def download_files():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        
    for file_path in FILES:
        url = BLOCKLY_BASE_URL + file_path
        local_path = os.path.join(TARGET_DIR, os.path.basename(file_path))
        
        print(f"Downloading {url} to {local_path}...")
        try:
            urllib.request.urlretrieve(url, local_path)
            print("Done.")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

if __name__ == "__main__":
    download_files()
