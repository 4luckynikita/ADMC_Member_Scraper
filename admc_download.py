

import os
import requests
from bs4 import BeautifulSoup
from time import sleep
import random

BASE_URL = "https://admc.net/members"
OUTPUT_DIR = "admc_members"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_main_list_page():
    print(f"[+] Fetching main member directory page...")
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print(f"[!] Failed to fetch main page: {response.status_code}")
        return None

    file_path = os.path.join(OUTPUT_DIR, "list_main.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    return file_path

def extract_profile_links_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    links = [a["href"] for a in soup.select(".member-grid-item a")]
    print(f"[DEBUG] Found {len(links)} profile URLs")
    return links

def download_profile_pages(profile_urls):
    for i, url in enumerate(profile_urls):
        filename = os.path.join(OUTPUT_DIR, f"profile_{str(i).zfill(3)}.html")
        if os.path.exists(filename):
            print(f"[-] Skipping already downloaded: {filename}")
            continue
        try:
            print(f"[+] Downloading profile {i+1}/{len(profile_urls)}: {url}")
            response = requests.get(url)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            sleep(random.uniform(1, 3))
        except Exception as e:
            print(f"[!] Failed to download {url}: {e}")

def main():
    list_page_path = fetch_main_list_page()
    print(f"[DEBUG] list_page_path = {list_page_path}")
    if list_page_path and os.path.exists(list_page_path):
        print("[DEBUG] Proceeding to extract and download profile pages...")
        profile_urls = extract_profile_links_from_file(list_page_path)
        download_profile_pages(profile_urls)
    else:
        print("[!] list_main.html does not exist or was not fetched correctly.")

if __name__ == "__main__":
    main()