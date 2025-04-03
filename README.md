# ADMC Member Scraper

This is a small Python script I wrote to scrape member information from the ADMC (Academy of Dental Management Consultants) website.

The goal was to grab the names, emails, phone numbers, addresses, websites, and Facebook profiles of all listed members, and save it into a CSV for later use.

---

## How it works

There are two parts:

### 1. `admc_download.py`
- Downloads the main member directory page
- Finds all individual profile links
- Downloads each profile page to `admc_members/`

### 2. `admc_parser.py`
- Reads through all the downloaded profile HTML files
- Parses out the important details
- Exports everything to `admc_members.csv`

---

## How to run

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the downloader:
   ```bash
   python admc_download.py
   ```

3. Run the parser:
   ```bash
   python admc_parser.py
   ```

That's it! You should end up with a nicely formatted CSV of all member data.

---

## Notes

- I added a `.gitignore` to exclude the CSV and the downloaded HTML files.
- This was mainly a practice project to get more comfortable with `requests`, `BeautifulSoup`, and just scripting things out cleanly.
