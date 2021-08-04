
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


def lcs_driver(combos):
    for pair in combos:
        word1 = pair[0]
        word2 = pair[1]
        # Ignore the same value
        if word1 == word2:
            pass
        # And inversions.
        if (tried.get(word1 + word2) is not None) or (tried.get(word2 + word1) is not None):
            continue
        else:
            # Add i=j and j=i to the dictionary to make sure we don't call LCS on it later.
            tried[word1 + word2], tried[word2 + word1] = 1, 1      

        holder = lcs(word1, word2) 

        if urls.get(holder) is not None:
            urls[holder] += 1
        else:
            urls[holder] = 1



# Maintaining 2 dictionaries in the driver.
# As well as an n-length list using a n^2 loop.
def driver(wordlist):
    global urls
    global tried

    urls = {}
    tried = {}
    import itertools
    from multiprocessing.pool import ThreadPool
    # Goes over the wordlist to find all combinations of words that we will run across.
    combos = [ combo for combo in itertools.combinations(wordlist,2)]

    # Cut combos into a list of n/10
    # Run pool.apply_async on each slide

    pool = ThreadPool(processes=5)
    slices = len(combos)//5
    async_result = pool.apply_async(lcs_driver(combos[:slices]))
    async_result = pool.apply_async(lcs_driver(combos[slices:slices*2]))
    async_result = pool.apply_async(lcs_driver(combos[slices*2:slices*3]))
    async_result = pool.apply_async(lcs_driver(combos[slices*3:slices*4]))
    async_result = pool.apply_async(lcs_driver(combos[slices:]))
    
    return urls
