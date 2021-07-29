'''
dataset_utility.py
This file contains helper functions for interacting with datasets and curing data.
Will contain generic functions in the future to interact with a broad array of data inputs.
'''
def import_json(dataset):
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
    # Going over the PhishTank json data to find unique IPs.
    return ips

def data_to_excel(data, column):
    import pandas as pd
    from pandas import ExcelWriter
    from pandas import ExcelFile
    # change IPs to the generic later
    df = pd.DataFrame({'IPs':list(set(ips))})
    # This saves those unique IPs to a spreadsheet.
    # Could definitely do a lot here.
    writer = ExcelWriter('PhishTank-IPs.xlsx')
    df.to_excel(writer,column,index=False)
    writer.save()

# Data Curing Function Should Go Here
def domain_cure(results, flag, count):
    # List our prevalanet domains.
    domains = []
    with open(results) as file:
        urls = []
        # Go over the input file and only add the count we want to urls array.
        data = file.readlines()
        for entry, value in enumerate(data):
            if entry >= count:
                break
            urls.append(value.strip())
        # Enumerate over the URLs.
        for entry,value in enumerate(urls):
            try:
                # Strip out the http://.
                new_value = value.split("//", 1)[1]
                #Split on the end of the TLD.
                new_value = new_value.split("/",1)
                if flag.lower() == "domain":
                    # Split the entry and append the TLD, then break out of loop.
                    domains.append(new_value[0])
                    break
                elif flag.lower() == "path":
                    val_length = len(new_value[1])
                    if len(new_value[1]) > 2 and len(new_value[1]) < 80:
                        domains.append(new_value[1])
            except:
                #If an error happens, ignore the input.
                pass
    return domains
