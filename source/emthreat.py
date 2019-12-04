import numpy as np
import requests
from time import sleep
from bs4 import BeautifulSoup
from lcs import driver
from time import perf_counter as timer
import matplotlib.pyplot as plt
import sys
'''
EmThreat is a tool to help web admins notice spikes in phishing activity
for software that they use by analyzing the URLs on PhishTank
and comparing them to URLs used by the admin.

Many websites have similar URL paths because they use the same software
so if many URLs pop up on PhishTank that match the ones used by a web admin,
that software may have a new exploit targeting it.

Usage:

python3 EmThreat.py [number of URLs to parse] [db_file]
'''

def online_url_fetch(pages):
    # Fetches recently reported phishing sites.
    # Do not use too much to prevent heavy site traffic.
    page = 1
    # check_url = "https://checkurl.phishtank.com/checkurl/"
    online_words = []
    phish_id = 0
    while page < pages:
        search_url = f"https://www.phishtank.com/phish_search.php?page={page}&active=y&verified=u"
        r = requests.get(search_url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            try:
                # Messy but works!
                for table in soup.find_all('table'):
                    for row in table.find_all("td"):
                        # User profiles call user.php instead of full links
                        # So this filters out stuff wr don't need

                        # Grab id of current phish
                        if len(row.text) == 7 and row.text != "Unknown":
                            phish_id = row.text
                        # Grab the link
                        if "http" in row.text:
                            # If it is hidden, we have to go to the page directly
                            if "..." in row.text:
                                phish_url = f"https://www.phishtank.com/phish_detail.php?phish_id={phish_id}"
                                search_phish = requests.get(phish_url)
                                if search_phish.status_code == 200:
                                    search_soup = BeautifulSoup(search_phish.text, 'html.parser')
                                    style = "word-wrap:break-word;"
                                    res = search_soup.find_all("span", attrs={"style": style})[0].text.split("//")[1]
                                    online_words.append(res)
                            else:
                                # print(row.text.split(" ")[0])
                                online_words.append(row.text.split(" ")[0].split("//")[1])
            except:
                print("No table found.")
        else:
            sleep(2)
        page += 1


def local_url_fetch(entries, db):
    # Fetches phishing URLs from a local database.
    import json
    urls = []
    with open(db) as file:
        data = json.load(file)

    # We want to split out the https/http since they are too common.
    for url in range(min(entries, len(data))):
        urls.append(data[url]['url'].split("//")[1])

    return urls


def write_urls(file_name, urls):
    # Write select URLs to a file.
    with open(file_name, "w") as f:
        for url in urls:
            f.write(url + "\n")


def demo_fetch(entries, db):
    # Pulls URLs from a text file as opposed to json.
    # Good for demos where we do not have the space to store an entire DB.
    urls = []
    with open(db) as file:
        for count, value in enumerate(file):
            if count == entries:
                break
            urls.append(value.strip())
    return urls


if __name__ == "__main__":
    # Use the local_url_fetch if you are storing the db.
    # words = local_url_fetch(400, 'verified_online.json')
    # Otherwise we can write a subset of URLs to a smaller file.
    # write_urls("test1", words)
    args = sys.argv
    total_urls = args[1]
    db_file = str(args[2])
    words = demo_fetch(total_urls, db_file)
    start = timer()
    results = driver(words)
    end = timer()
    diff = end - start
    print(f'Finished in {diff / 60} minutes\n')
    for p in results:
        if len(p) > 5 and "/" in p:
            print(p)

    # Graphing madness below!
    N = np.arange(10)
    # These list comprehensions are crazy!
    graph_results = sorted([results[x] for x in results if len(x) > 5 and "/" in x])[-10:]
    graph_ticks = sorted([x for x in results if len(x) > 5 and "/" in x])[-10:]
    # If a URL is too long...
    for i, v in enumerate(graph_ticks):
        if len(v) > 30:
            graph_ticks[i] = v[:30] + "..."

    spacing = 1
    # Adding the URLs to the bar chart.
    for i, x in enumerate(graph_results):
        plt.bar(spacing * i, height=x, tick_label="")
    # This was a cool solution but the URLs were still too long.
    # plt.xticks(N, graph_ticks, rotation=70)
    plt.legend(graph_ticks)
    plt.ylabel('Count')
    plt.xlabel('URLs')
    plt.title('Phishing URLs')
    plt.show()
