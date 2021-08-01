
'''
lcs.py
This code is used to handle the longest common substring algorithm and a driver that will go over a wordlist
and compute a dictionary containing the most common substrings using SequenceMatcher.

The driver function is used to keep track of URLs.
'''

# SequenceMatcher implementation to return the longest match.
def lcs(s1, s2):
    from difflib import SequenceMatcher
    seq = SequenceMatcher(None, s1, s2)
    lcs = seq.find_longest_match(0, len(s1),0, len(s2))
    if (lcs.size != 0):
    	return str(s1[lcs.a: lcs.a + lcs.size])
    else:
    	return ""

# Maintaining 2 dictionaries in the driver.
# As well as an n-length list using a n^2 loop.
def driver(wordlist):
    urls = {}
    tried = {}
    # Goes over the wordlist to find all combinations of words that we will run across.
    for word1 in wordlist:
        for word2 in wordlist:
            # Ignore duplicates.
            if word1 == word2:
                continue
            # And inversions.
            if (tried.get(word1 + word2) is not None) or (tried.get(word2 + word1) is not None):
                continue
            else:
                # Add i=j and j=i to the dictionary to make sure we don't call LCS on it later.
                tried[word1 + word2], tried[word2 + word1] = 1, 1

            # Store the longest common substring.
            # Will either be a string or '0'
            holder = lcs(word1, word2)

            # If the substring already exists we increment it
            # otherwise we insert it.
            if urls.get(holder) is not None:
                urls[holder] += 1
            else:
                urls[holder] = 1

    return urls
