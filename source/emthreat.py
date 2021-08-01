#!/usr/bin/env python3
import requests
import sys
import argparse

from lcs import driver
from time import perf_counter as timer


import chunking
import dataset_utility
import fetch

import matplotlib.pyplot as plt

'''
EmThreat is a tool to help web admins notice spikes in phishing activity
for software that they use by analyzing the URLs on PhishTank
and comparing them to URLs used by the admin.

Many websites have similar URL paths because they use the same software
so if many URLs pop up on PhishTank that match the ones used by a web admin,
that software may have a new exploit targeting it.

python3 EmThreat.py --help
'''

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
    for block in blocks:
        # LCS returns a dictionary.
        words = driver(block)
        results.append(words)
    return results

# Prints out results to the command line.
def print_output(results):
    # Store the results that we want in a new 2D array.
    new_results = loop_dict(results) 
    print(f"{len(new_results)} results found after cleaning output.")
    for pair in new_results:
        print(f"URL:{pair[0]} Count: {pair[1]}")

# Saves output to a file.
def save_output(results, file_name):
    with open(file_name, "w+") as file:
        new_results = loop_dict(results)
        for pair in new_results:
                file.write(f"URL:{pair[0]} Count: {pair[1]}\n")
        print(f"Wrote {len(new_results)} to {file_name}")

# Loops over a dictionary to get URLs that meet our basic criteria.
def loop_dict(results):
    # Grab total of all dictionaries.
    reslen = sum(len(block) for block in results) 
    print(f"EmThreat has found {reslen} common substrings.")
    # Min frequency and length
    new_results = []
    freq = 10
    minlength = 5
    print(f"Searching for substrings that appear more than {freq} times and are longer than {minlength} characters.")
    for pair in results:
        # For each pair in the dictionary.
        for value, count in pair.items():
            # If the URL appears enough times and is longer than a few characters.
            if count > freq and len(value) > minlength:
                new_results.append([value, count])
    
    # Send 2D array to directory_elim
    directory_only = directory_elim(new_results)
    # Returns 2D array of paths that only have directories and their counts. 
    return directory_only

def directory_elim(results):
    # Input is a 2D array
    # [value, count]
    new_results = []
    for pair in results:
        path = pair[0]
        # If the path contains a directory level, append it. 
        is_directory_level = dataset_utility.high_level(path)
        if is_directory_level:
            new_results.append(pair)
    return new_results

if __name__ == "__main__":
    # Using ArgumentParser to handle our arguments.
    parser = argparse.ArgumentParser(description='EmThreat 1.1 is a tool to help web admins notice spikes in phishing activity for software \
        that they use by analyzing the URLs on PhishTankand comparing them to URLs used by the admin.')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-f', help="db_file: The file that URLs will be read from.")
    parser.add_argument('-c', help="total_urls: The amount of URLs that will be processed.")
    parser.add_argument('-i', default="txt", choices=["csv", "json", "txt"], help="Input: Determines the file type of the database used.")
    group.add_argument('-o', default = "print", choices=["print", "save"], help="Output: Determines if saved to a file or printed to screen.")
    parser.add_argument('-n', default ="report.txt", help="Name: The name that the report file will be saved as.")
    args = parser.parse_args()

    # Variables to store main actions we will take.
    total_urls = int(args.c)
    db_file = str(args.f)
    db_type = str(args.i)
    # Report type and output.
    report_output = str(args.o)
    report_name = str(args.n)

    # An array of URLs extracted from supported file types.
    urls = fetch.open_database(db_file, total_urls, db_type)

    # Grabs just the paths from the URLs.
    words = dataset_utility.path_clean(urls)
    start = timer()
    # Turns words into blocks.
    blocks = chunking.block_gen(words)
    # Runs LCS on each block.
    results = block_lcs(blocks)
    end = timer()
    diff = end - start
    print(f'Finished in {diff / 60} minutes\n')

    # Handle what we do after reaching our results.
    if report_output == "print":
        print_output(results)
    else:
        save_output(results, report_name)
    # Graphing output will become an option after 1.5 or so.
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
