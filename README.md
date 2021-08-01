![EmThreat Logo](https://imgur.com/Hv703W4.png)


# About EmThreat 1.1
Threat Intelligence tool utilizing a CLI interface to detect emerging threats by analyzing reports from PhishTank. Download the dataset at [PhishTank's website.](https://www.phishtank.com/developer_info.php)

The goal of this tool is to quickly analyze the most common paths of phishing websites, which can be used to classify recently vulnerable software and provide immediate warning to security teams before wide-scale attacks are reported.

This is built off of the amazing research done by [UAB's Center for Cyber Security](https://www.uab.edu/cas/thecenter/images/Documents/Identifying-Vulnerable-Websites-by-Analysis-of-Common-Strings-in-Phishing-URLs.pdf)

# What we want out of intelligence
- Domain & Paths
- Submission Time to understand trends over time
  - Such as geographic location or software used in compromised sites.
- Details Array containing a dict with ip_address, cidr_block, country

### Dependency list:
- bs4
- matplotlib

### Usage:
`usage: emthreat.py [-h] [-f F] [-c C] [-i {csv,json,txt}] -o {print,save}
                   [-n N]`

optional arguments:

  -h, --help         show this help message and exit
  
  -f F               db_file: The file that URLs will be read from.
  
  -c C               total_urls: The amount of URLs that will be processed.
  
  -i {csv,json,txt}  Input: Determines the file type of the database used.
  
  -o {print,save}    Output: Determines if saved to a file or printed to screen.
  
  -n N               Name: The name that the report file will be saved as.

## Contributing
emthreat.py is the main driver file that handles arguments, calls functions from supporting libraries, and executes the output.

lcs.py handles the longest-common-substring code. It also has a driver to iterate over a combination of every possible input. This needs to have a suffix tree implementation added to considerably speed up  the n\*m computation time.

dataset_utility.py cleans up the URLs and has code for interacting with XLS files.

chunking.py holds functions to break up large datasets to improve the speed of lcs.py. 

fetch.py holds functions for interacting with PhishTank and pulling data from local files.
