![EmThreat Logo](https://imgur.com/Hv703W4.png)

# About
Threat Intelligence tool used to detect emerging threats by analyzing reports from PhishTank. Download the dataset at [PhishTank's website.](https://www.phishtank.com/developer_info.php)

The goal of this tool is to quickly analyze either the most common domains or their paths, the latter of which can be used to classify recently vulnerable software and provide immediate warning to security teams before wide-scale attacks are reported.

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
`python3 emthreat.py [number of urls] [input file] {domain, path}`

Specify the number of URLs you want to scan out of a CSV file, the path to the CSV file, and whether you want to output the most common domains or paths.

Please leave comments.

## Contributing
emthreat.py is the main file, it handles the processing of information from a locally downloaded database. In the future this data handling can be done in a separate library as more features are added.

lcs.py handles the longest-common-substring code. It also has a driver to iterate over a combination of every possible input. This needs to have a suffix tree implementation added to considerably speed up  the n\*m computation time.

dataset_utility.py has some minor code that I use for manipulating the database directly in order to see what kind of information might be useful to analysts. Feel free to add functions to it that automate in report tasks or help in parsing the datasets. 

chunking.py holds functions to break up large datasets to improve the speed of lcs.py. 
