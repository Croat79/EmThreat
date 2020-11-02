#!/usr/bin/env python3
import requests
from time import sleep
from bs4 import BeautifulSoup
from lcs import driver
from time import perf_counter as timer
import matplotlib.pyplot as plt
import sys

## TODO Break online_url_fetch into different functions
## TODO Implement additional utilities to graph IPs

'''
EmThreat is a tool to help web admins notice spikes in phishing activity
for software that they use by analyzing the URLs on PhishTank
and comparing them to URLs used by the admin.

Many websites have similar URL paths because they use the same software
so if many URLs pop up on PhishTank that match the ones used by a web admin,
that software may have a new exploit targeting it.

Usage:

python3 EmThreat.py [number of URLs to parse] [db_file] [filter]
'''
# Headers to append to any request.
ID = "YOUR PHISHTANK ID"
headers = {"user-agent": "phishtank/" + str(ID)}


def online_url_fetch(pages):
    # Fetches recently reported phishing sites.
    page = 1
    pause = 2
    # check_url = "https://checkurl.phishtank.com/checkurl/"
    online_words = []
    phish_id = 0
    while page < pages:
        search_url = f"https://www.phishtank.com/phish_search.php?page={page}&active=y&verified=u"
        r = requests.get(search_url, headers=headers)
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
                                search_phish = requests.get(phish_url, headers=headers)
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
            # Give the server a break
            sleep(pause)
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

def csv_fetch(entries, db):
    # Opens a csv file and fetches information.

    # Split by comma
    urls = []
    with open(db) as file:
        for count, url in enumerate(file):
            if count == entries:
                break
            try:
                urls.append(url.split(",")[1].split("//")[1])
            except:
                pass

    return urls

def write_urls(file_name, urls):
    # Write select URLs to a file.
    with open(file_name, "w") as f:
        for url in urls:
            f.write(url + "\n")


def demo_fetch(entries, db):
    # Pulls URLs from a text file as opposed to json.
    # Good for demos where we do not have the space or time to store an entire DB.
    urls = []
    with open(db) as file:
        for count, value in enumerate(file):
            #print(type(entries))
            if count == entries:
                break
            urls.append(value.strip())
    return urls

def split_url(url, filter):
    # Helper function to split a URL into the domain or software path.
    tmp = url.split("/", 1)
    if filter == "domain":
        return tmp[0]
    elif filter == "path":
        if len(tmp) > 1:
            return tmp[1]
        else:
            # There is no path.
            return ''
    else:
        # Could return a default value like domain.
        print("Invalid filter. Returning full URL.")
        return tmp

def filter_input(wordlist, url_filter):
    # Goes over a wordlist and splits the urls.
    tmp = []
    for word in wordlist:
        tmp.append(split_url(word, url_filter))
    # Removes None values.
    return list(filter(None, tmp))

def build_graph(results, names, url_filter):
    spacing = 3
    start_of_text = (max(results)/100) * 2 #Places test 2% in every time.
    # Adding the URLs to the bar chart.
    for i, x in enumerate(results):
        plt.barh(spacing * i, height=2, width=x)
    for j, v in enumerate(names):
        plt.text(start_of_text, spacing * j, str(v), color='black', fontweight='bold', verticalalignment='center')
    # Making sure yticks are empty
    plt.yticks([], [])
    # Adding out labels
    plt.ylabel('URLs')
    plt.xlabel('Count')
    plt.title(f'Phishing Threats by {url_filter.title()}')
    plt.show()


if __name__ == "__main__":
    # Use the local_url_fetch if you are storing the db. (primarily for demo purposes)
    # words = local_url_fetch(400, 'verified_online.json')
    # Otherwise we can write a subset of URLs to a smaller file.
    # write_urls("test1", words)
    args = sys.argv
    total_urls = int(args[1])
    db_file = str(args[2])
    url_filter = str(args[3]) # Path or domain
    # Call a function to split and grab either the url or path
    words = demo_fetch(total_urls, db_file)
    words = filter_input(words, url_filter)

    start = timer()
    results = driver(words)
    #print(results)
    end = timer()
    diff = end - start
    print(f'Finished in {diff / 60} minutes\n')
    # Below is demo code to only print out results that are long and have slashes, indicating paths.
    '''
    for p in results:
        if len(p) > 5 and "/" in p:
            print(p)
    '''
    total_matches = 10
    min_output_length = 5
    # Sort our results and then store the top X key/value pairs.
    # Filter results for faster outputs
    results = {k:v for (k,v) in results.items() if len(k) > min_output_length}
    graph_results = sorted(results.values())[-total_matches:]
    graph_ticks = sorted(results.keys())[-total_matches:]
    #print(results)
    # If a URL is too long...
    for i, v in enumerate(graph_ticks):
        if len(v) > 30:
            graph_ticks[i] = v[:30] + "..."
    build_graph(graph_results, graph_ticks, url_filter)
