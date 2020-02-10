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

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

df = pd.DataFrame({'IPs':list(set(ips))})

writer = ExcelWriter('PhishTank-IPs.xlsx')
df.to_excel(writer,'IPs',index=False)
writer.save()

# What we want out of intelligence
# - Domain (everything between // and /. If no second / exists grab split(//)[1])
# - Software path (everything after /)
# - submission_time to understand trends over time
# - Details Array containing a dict with ip_address, cidr_block, country

# I'll want a list of IPs on their own anyways
# 4397 IPs!
