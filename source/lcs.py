## TODO Speed up LCS using suffix trees
# Once EmThreat allows for domain/software path filtering we can drastically reduce runtime even further.

'''
This code is used to handle the longest common substring algorithm and a driver that will go over a wordlist
and compute a dictionary containing the most common substrings.
'''
def fast_lcs(first, second):
    m = len(first)
    n = len(second)
    # Build a 2D array to store the comparison values.
    match_matrix = [[0 for x in range(n+1)] for y in range(m+1)]
    start, end = 0, 0
    length = 0
    skip = False

    # Go over the first word
    for i in range(1, m + 1):
        # Go over the second word
        for j in range(1, n + 1):
            # If the previous characters match in both words
            if first[i-1] == second[j-1]:
                # Set the current ij value to an increment of the previous.
                match_matrix[i][j] = match_matrix[i-1][j-1] + 1
                # If this value is greater than our stored length
                # then the new substring is the longest
                if length < match_matrix[i][j]:
                    length = match_matrix[i][j]
                    start, end = i, j

    # If length is 0, we do not need to perform the while loop
    # and can just return a string that says '0'
    if length == 0:
        return '0'

    substring = ""
    # Go diagonally through the 2d array to find the values of the
    # longest common substring.
    while match_matrix[start][end] > 0:
        substring += first[start-1]
        start, end = start - 1, end - 1

    # Flip the result since it is backwards.
    return substring[::-1]

def new_lcs(s1, s2):
    from difflib import SequenceMatcher
    s = SequenceMatcher(None, s1, s2)
    lcs = ''.join([s1[block.a:(block.a + block.size)] for block in s.get_matching_blocks()])
    return lcs

# Maintaining 2 dictionaries in the driver.
# As well as an n-length list using a n^2 loop.
## TODO Find optimizations.
def driver(wordlist):
    urls = {}
    tried = {}
    # Goes over the wordlist to find all combinations of words that we will run across.
    for i in wordlist:
        for j in wordlist:
            # Ignore duplicates.
            if i == j:
                continue
            # And inversions.
            if (tried.get(i + j) is not None) or (tried.get(j + i) is not None):
                continue
            else:
                # Add i=j and j=i to the dictionary to make sure we don't call LCS on it later.
                tried[i + j], tried[j + i] = 1, 1

            # Store the longest common substring.
            # Will either be a string or '0'
            holder = new_lcs(i, j)

            # If the substring already exists we increment it
            # otherwise we insert it.
            if urls.get(holder) is not None:
                urls[holder] += 1
            else:
                urls[holder] = 1

    return urls
