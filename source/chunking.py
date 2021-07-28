'''
Chunking will do the following
- data should be sorted before chunking to allow better representation
- creating blocks of size 1000
- each block will have LCS run on it
- the top 100 results from each block are saved to a new list
- finds the top 100 most occuring results
'''
import math

# Returns an array of X blocks.
# If 1000 results are passed to 10 blocks, then each block has 100 results. 
# [[block1], [block2],...[blockn]]
# [[url11, url12, url1n],...[urln1, urln2, urlnn]]
def block_gen(results):
    block_length = 10 # 10 for testing
    # Calculate the total blocks used.
    block_total = math.ceil(len(results) / block_length)
    # Create a 2D array to store blocks.
    # [[block1], [block2],...[blockn]]
    blocks = [] * block_total
    # Go over each new block.
    for i in range(0, len(results), block_length):
        # Iterate over the range of i to the block length. 
        for j in range(i, i + block_length ):
            # Go to the ith block and append the jth URL from results.
            blocks[i//block_total].append(results[j])
    # Test output of blocks
    return blocks

def block_lcs(blocks):
    results = [] * (len(blocks) + 1)
    for i in blocks:
        # run lcs on block_gen(results)
        # results[i] = results
        pass
    # return results
    
# - the top 20 results from each block are saved to a new list
# - finds the top 100 most occuring results

def sort_block_results(results):
    sorted_results = []
    for i in results:
        # sort the results to find top 20 and add them to sorted_results

        pass
    return sorted_results

def top_100_results(results):
    return results[:100]


def driver():
    blocks = block_gen(results)
    results = block_lcs(blocks)
    sorted_results = sort_block_results(results)
    final_results = top_100_results(sorted_results)
    return final_results

    
