
'''
lcs.py
This code is used to handle the longest common substring algorithm 
and a driver that will go over an input of URL paths.

The result is a dictionary of paths and the count of times they have been seen.
'''
from time import perf_counter as timer

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
    # This is a driver that runs in async with other threads.
    # It will run over a subset of the combo list.
    for pair in combos:
        # For each combo, we grab the 2 URLs in it.
        word1 = pair[0]
        word2 = pair[1]
        # Ignore the same value
        if word1 == word2:
            pass
        # And inversions. This way we dont compute the same pair in reverse order.
        if (tried.get(word1 + word2) is not None) or (tried.get(word2 + word1) is not None):
            continue
        else:
            # Add i=j and j=i to the dictionary to make sure we don't call LCS on it later.
            tried[word1 + word2], tried[word2 + word1] = 1, 1      

        # Run the actual LCS function on this.
        holder = lcs(word1, word2) 

        # If we have already seen a substring, its count is incremented.
        if urls.get(holder) is not None:
            urls[holder] += 1
        # Otherwise it is added.
        else:
            urls[holder] = 1



# Maintaining 2 dictionaries in the driver.
# As well as an n-length list using a n^2 loop.
def driver(wordlist):
    start = timer()
    # Using globals so the async threads update the dictionaries
    # otherwise we could get race conditions
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

    # Now that this works, lets dynamically create threads based 
    # on thread count + slices
    threads = 5
    slices = len(combos)//threads

    pool = ThreadPool(processes=threads)

    #Create our threads..except the last one.
    for thread in range(threads - 1):
        # This will give us 10 * 0 on the first thread
        # and 10 * 1 on the second
        # etc
        current = slices * thread
        next_section = slices * (thread + 1)
        #print(f"{current}:{next_section}")
        # Each thread will be [0:10], [10:20], etc 
        # with the number being based on length / 10
        pool.apply_async(lcs_driver(combos[current:next_section]))


    # Create the final thread
    pool.apply_async(lcs_driver(combos[slices:]))

    # We could store the result of these async threads in a variable
    # but nothing is being returned because we use globals.
    end = timer()
    diff = end - start
    print(f'LCS block finished in {diff / 60} minutes\n') 
    return urls
