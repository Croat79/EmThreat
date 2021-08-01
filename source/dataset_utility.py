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


# Pull out just the paths of URLs.
def path_clean(urls):
    # List our prevalent paths.
    paths = []
    min_length = 2
    max_length = 80
       
    # Go over URLs array and only append values that meet our criteria.
    for value in urls:
        try:
            # Strip out the http://.
            # We can move this part to a function too
            new_value = value.split("//", 1)[1]
            #Split on the end of the TLD.
            new_value = new_value.split("/",1)
            val_length = len(new_value[1])
            if len(new_value[1]) > min_length and len(new_value[1]) < max_length:
                paths.append(new_value[1])
        except:
            #If an error happens, ignore the input.
            pass
    return sorted(paths)
