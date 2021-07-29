#!/usr/bin/env python3
import requests
from time import sleep
from bs4 import BeautifulSoup
from lcs import driver
from time import perf_counter as timer
import matplotlib.pyplot as plt
import sys
import chunking
import dataset_utility


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

# Mostly a debugging function but can be used in the future to assist with reporting.
def write_urls(file_name, urls):
    # Write select URLs to a file.
    with open(file_name, "w") as f:
        for url in urls:
            f.write(url + "\n")

# Build a graph from the results and our filter.
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

# Run LCS on blocks.
def block_lcs(blocks):
    # Create an array to store the dictionary outputs.
    results = []
    for i in blocks:
        # LCS returns a dictionary.
        words = driver(i)
        results.append(words)
    return results

if __name__ == "__main__":
    args = sys.argv
    total_urls = int(args[1])
    db_file = str(args[2])
    url_filter = str(args[3]) # Path or domain
    # Call a function to split and grab either the url or path
    words = dataset_utility.domain_cure(db_file, url_filter, total_urls)
    #print(words[:100])
    #print(len(words))
    start = timer()
    blocks = chunking.block_gen(words)
    results = block_lcs(blocks)
    #Uncomment below to store a text file of example data.
    '''
     with open("temp.txt", "w+") as file:
        for i in results:
            for j, v in i.items():
                if v > 100 and len(j) > 5:
                    file.write(f"URL:{j} Count: {v}")
                    file.write("\n")
    '''
    end = timer()
    diff = end - start
    print(f'Finished in {diff / 60} minutes\n')

    ## TODO Now that the results is an array of dictionaries, we have to handle graphing slightly differently.
    ## TODO Replace these values with variables that can be overidden by optional flags.
    ## TODO Put graphing in its own library.
    '''
    total_matches = 10
    min_output_length = 5
    # Sort our results and then store the top X key/value pairs.
    # Filter results for faster outputs
    # should no longer need to check for min output length hopefully
    # or can bake this into LCS so it has a minimum length to accept
    results = {k:v for (k,v) in results.items() if len(k) > min_output_length}
    graph_results = sorted(results.values())[-total_matches:]
    graph_ticks = sorted(results.keys())[-total_matches:]
    #print(results)
    # If a URL is too long...
    for i, v in enumerate(graph_ticks):
        if len(v) > 30:
            graph_ticks[i] = v[:30] + "..."
    build_graph(graph_results, graph_ticks, url_filter)
    '''
