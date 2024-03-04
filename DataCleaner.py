import pandas as pd
import requests

# importing initial data, extracting relevant columns and sorting context alphabetically to group by context
df = pd.read_csv('new_data.csv')
columnsToExtract = ['phrase', 'type', 'start_index', 'end_index', 'context']
extractedDF = df[columnsToExtract]
dfAlphabetical = df.sort_values(by= 'context')

# removing identical rows
dfAlphabetical = dfAlphabetical.drop_duplicates()

# downloading sorted dataset
dataSorted = dfAlphabetical.to_csv()
with open('data.csv', 'w') as f:
    f.write(dataSorted)
url = 'http://example.com/data.csv'  
response = requests.get(url)
with open('downloaded_data.csv', 'wb') as f:
    f.write(response.content)

# merging identical contexts