![EmThreat Logo](https://imgur.com/Hv703W4.png)

# 1.0 Release set for ~~11/3/2020~~


## ROADMAP
The tool currently utilizes demo-functionality in a CLI inferace. Many of the functions are not clear and use cases are niche. 

We are working on implementing a user interface for easy use as well as improving the performance of the tool on larger datasets.

The biggest feature of the tool, which might not be added until a later release, will be taking in information from various formats besides CSV and JSON. Users will be able to deliminate their fields to ensure information is parsed correctly. 

If there are any feature requests, please create a new issue for now. The plan is to continue iterating on the 'demo version' in production, then present it to get user feedback.


## ABOUT

Threat Intelligence tool used to detect emerging threats by analyzing reports from various open source outlets.

The goal of this tool is to quickly analyze either the most common domains or their paths, the latter of which can be used to classify recently vulnerable software and provide immediate warning to security teams before wide-scale attacks are reported.

Currently set in demo-mode. The 1.0 release will add additional options.

Dependency list:
- numpy
- bs4
- matplotlib

Usage:
`python3 emthreat.py [number of urls to scan] [input file]`

Please leave comments.
