

import os
from bs4 import BeautifulSoup
import csv

# Directory containing profile HTML files
PROFILE_DIR = "admc_members"
OUTPUT_CSV = "admc_members.csv"

def parse_profile(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    name_tag = soup.find("h1", class_="entry-title")
    name = name_tag.get_text(strip=True) if name_tag else ""

    practice_tag = soup.find("h2", class_="member-practice-name")
    practice_name = practice_tag.get_text(strip=True) if practice_tag else ""

    phone_tag = soup.find("li", class_="member-phone-number")
    phone = phone_tag.get_text(strip=True).replace("Phone: ", "") if phone_tag else ""

    email_tag = soup.find("a", href=lambda href: href and "mailto:" in href)
    email = email_tag["href"].replace("mailto:", "") if email_tag else ""

    website_tag = soup.find("a", href=True, text=lambda t: t and "Visit Website" in t)
    website = website_tag["href"] if website_tag else ""

    address_tag = soup.select_one("li i.fal.fa-map-marker-alt + a")
    address = address_tag.get_text(" ", strip=True) if address_tag else ""

    social_tag = soup.select_one("div.member-social-icons a[href*='facebook.com']")
    facebook = social_tag["href"] if social_tag else ""

    return {
        "Name": name,
        "Practice": practice_name,
        "Phone": phone,
        "Email": email,
        "Website": website,
        "Address": address,
        "Facebook": facebook
    }

def main():
    rows = []
    for filename in os.listdir(PROFILE_DIR):
        if filename.startswith("profile_") and filename.endswith(".html"):
            filepath = os.path.join(PROFILE_DIR, filename)
            row = parse_profile(filepath)
            rows.append(row)

    # Write to CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Name", "Practice", "Phone", "Email", "Website", "Address", "Facebook"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[+] Successfully wrote {len(rows)} members to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()