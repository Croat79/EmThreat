![EmThreat Logo](https://imgur.com/Hv703W4.png)

Phishing Intelligence tool used to detect emerging threats by analyzing reports from PhishTank. Download the dataset at [PhishTank's website.](https://www.phishtank.com/developer_info.php)

The goal of this tool is to quickly analyze either the most common domains or their paths, the latter of which can be used to classify recently vulnerable software and provide immediate warning to security teams before wide-scale attacks are reported.

Dependency list:
- numpy
- requests
- time
- bs4
- matplotlib

Usage:
`python3 emthreat.py [number of urls to scan] [input file] {domain, path}`

Specify the number of URLs you want to scan out of a CSV file, the path to the CSV file, and whether you want to output the most common domains or paths.

Please leave comments.
