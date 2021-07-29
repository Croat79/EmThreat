'''
fetch.py

This library handles fetching information from online, downloading databses, etc.
It also contains old functions for interacting with data. 
Those will be generalized and moved to dataset_utility.py in 2.0
'''

# Headers to append to any request.
ID = "YOUR PHISHTANK ID"
headers = {"user-agent": "phishtank/" + str(ID)}


def online_url_fetch(pages):
    # Fetches recently reported phishing sites.
    print("Warning: Use web crawling responsibly and ensure you enter your Phishtank ID.")
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
        
# All 3 of the below functions use similar code.
# Should create a generic file opener function to load in data.
# Then a quick solution for parsing output based on the file.
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
