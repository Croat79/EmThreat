'''
fetch.py

This library handles fetching information from online, downloading databses, etc.
It also contains generic functions for interacting with data. 
'''
import json
# Headers to append to any request.
ID = "YOUR PHISHTANK ID"
headers = {"user-agent": "phishtank/" + str(ID)}
from bs4 import BeautifulSoup
import requests

## Testing these functions in 1.2
# Downloads fresh database (either CSV or JSON) from PhishTank.
def download_new_database(filetype, filename):
    # Fetches recently reported phishing sites.
    print("Warning: Use web crawling responsibly and ensure you enter your Phishtank ID.")
    url = "http://data.phishtank.com/data/online-valid" + str(filetype)
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        with open(filename, "wb") as file:
            file.write(r.content)
    else:
        print("Unable to download a new database. Have you used up your daily downloads?")

# Generic function to loop over a file and save the URLs to a new array.
def loop_data(file, entries, csv):
    urls = []
    for count, value in enumerate(file):
        if count == entries:
            break
        # If we have a CSV, split on commas.
        # PhishTank's CSV's have URLs in the 2nd column.
        if csv:
            urls.append(value.split(",")[1])
        # Else append normally.
        else:
            urls.append(value.strip())
    return urls

# Function to open a database based on the file type.
def open_database(db, entries, filetype):
    urls = []
    with open(db) as file:
        if filetype == "json":
            data = json.load(file)
            # Append data from JSON to the URLs array.
            for url in range(min(entries, len(data))):
                urls.append(data[url]['url'])
        elif filetype == "csv":
            urls = loop_data(file, entries, True)
        else:
            # Otherwise append normally.
            urls = loop_data(file, entries, False)
    return urls


# Check exploit DB for a software type
# check_exploitdb("wordpress")
# https://www.exploit-db.com/search?q=wordpress
# grab each date to see the latest vulns
# then print out those vulns
def check_exploitdb():
    pass