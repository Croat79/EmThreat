dataset = 'verified_online.json'
import json # Handling json file
ips= []
with open(dataset) as file:
	data = json.load(file)
	for entry in range(len(data)):
		try:
			ips.append(data[entry]["details"][0]["ip_address"]) # Grab IP addresses
		except: # Some entries are missing ip_address or are not formatted properly.
			pass
print(f"Unique IPs: {len(set(ips))}") # Use a set to find unique IPs
# This seems to go over the PhishTank json data to find unique IPs.
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

df = pd.DataFrame({'IPs':list(set(ips))})
# This saves those unique IPs to a spreadsheet.
# Could definitely do a lot here.
writer = ExcelWriter('PhishTank-IPs.xlsx')
df.to_excel(writer,'IPs',index=False)
writer.save()

# What we want out of intelligence
# - Domain (everything between // and /. If no second / exists grab split(//)[1])
# - Software path (everything after /)
# the above 2 could be used if the known list is not comprehensive enough
# but we can import that value anyways from a list of known TLDs 
# - submission_time to understand trends over time 
# - Details Array containing a dict with ip_address, cidr_block, country

# I'll want a list of IPs on their own anyways
# 4397 IPs!

# Data Curing Function Should Go Here
def domain_cure(results, flag):
	# List our prevalanet domains.
	known = [".xyz",".com",".net",".org",".live",".club",".uk", ".info", ".ga", ".tk", ".ml", ".cf"]
	domains = []
	with open(results) as file:
		data = file.read()
		for entry in range(len(data)):
			try:
				# Go over each known and see if it is in the entry URL.
				for i in known:
					if i in entry:
						if flag.lower() == "domain":
							# Split the entry and append the TLD, then break out of loop.
							domains.append(entry.split(i)[0] + i)
							break
						elif flag.lower() == "path":
							domains.append(entry.split(i)[1])
							break
			except: #If an error happens, ignore the input.
				pass
	#TODO: Test that this returns only domain with the 'domain flag'.
	#TODO: Test that this returns only paths with the 'path flag'.
	return domains
