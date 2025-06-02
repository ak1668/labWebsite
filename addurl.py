import time
import json
import requests
from bs4 import BeautifulSoup

# 1. Load and parse the input HTML
with open("publications.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# 2. Prepare Crossref query function
def find_doi(query):
    # Query Crossref works: title only, first result
    headers = {"User-Agent": "YourAppName/1.0 (mailto:you@example.com)"}
    params = {"query.bibliographic": query, "rows": 1}
    r = requests.get("https://api.crossref.org/works", params=params, headers=headers)
    if r.status_code == 200:
        items = r.json().get("message", {}).get("items", [])
        if items and "DOI" in items[0]:
            return items[0]["DOI"]
    return None

# 3. Iterate over each publication line (<li> or <p>)
for elem in soup.find_all(["li", "p"]):
    text = elem.get_text(strip=True)
    if not text or text[0].isdigit() is False:
        continue  # skip non‐publications
    print("Querying DOI for:", text[:60], "…")
    doi = find_doi(text)
    if doi:
        # Wrap the entire element content in an <a>
        a = soup.new_tag("a", href=f"https://doi.org/{doi}", target="_blank")
        a.string = text
        elem.string = ""
        elem.append(a)
        print("  → Found DOI:", doi)
    else:
        print("  → DOI not found")
    time.sleep(1)  # be kind to Crossref

# 4. Write out the updated HTML
with open("publications_with_doi1.html", "w", encoding="utf-8") as f:
    f.write(str(soup))

print("Done. Output written to publications_with_doi.html")
