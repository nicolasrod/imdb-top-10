# coding: utf8

# =============================================================
# Extract information from the Top 10 IMDB movies to a CSV file
# =============================================================

import csv
import requests

from bs4 import BeautifulSoup

# CSV file to generate
CSV_FILE = "top_movies.csv"

# Fake User Agent so IMDB does not return 403
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"
BASE = "https://www.imdb.com"

# IMDB movie chart
CHART = f"{BASE}/chart/top"


def get_url(url: str):
    """Fetch a URL faking the User Agent and returns the results as a string"""
    r = requests.get(url, headers={"User-Agent": USER_AGENT})

    if r.status_code != 200:
        raise RuntimeError(f"Error getting URL {url} - Status CODE: {r.status_code}")

    return r.text


def get_summary(href: str):
    """Fetch the page for the movie and extract the plot"""
    html = get_url(f"{BASE}{href}")
    bs = BeautifulSoup(html, "html.parser")
    plot = bs.find(attrs={"data-testid": "plot-xl"})
    return plot.get_text()


def main():
    """Extract the Top 10 movies from IMDB to a CSV file"""

    html = get_url(CHART)
    bs = BeautifulSoup(html, "html.parser")
    films = bs.find("table", class_="chart")

    print(f"[*] Extracting Top 10 IMDB Movies to {CSV_FILE}...", flush=True)

    with open(CSV_FILE, "w") as fd:
        fields = ["title", "rating", "summary"]
        w = csv.DictWriter(fd, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()

        # Get the first 10 table rows with movie information
        for row in films.tbody.find_all("tr", limit=10):
            tmp = row.find("td", class_="posterColumn")
            rating = round(
                float(tmp.find("span", attrs={"name": "ir"})["data-value"]), 1
            )

            tmp = row.find("td", class_="titleColumn")
            href = tmp.a["href"]
            title = tmp.a.text

            summary = get_summary(href)

            print(".", end="", flush=True)
            w.writerow(dict(title=title, rating=rating, summary=summary))

    print(flush=True)
    print("[*] Done!", flush=True)


if __name__ == "__main__":
    main()
