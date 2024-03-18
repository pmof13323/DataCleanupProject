import pandas as pd
import requests

# importing initial data, extracting relevant columns and sorting context alphabetically to group by context
df = pd.read_csv('new_data.csv')
columnsToExtract = ['phrase', 'type', 'start_index', 'end_index', 'context']
extractedDF = df[columnsToExtract]
dfAlphabetical = df.sort_values(by= 'context')

# removing identical rows
dfAlphabetical = dfAlphabetical.drop_duplicates()
dfAlphabetical.reset_index(drop=True, inplace=True)

# handling overlaps
indicesDrop = []
for index, row in dfAlphabetical.iterrows():
    if index > 0:
        prevRow = dfAlphabetical.iloc[index - 1]

        if row['context'] == prevRow['context']:

            overlap = not (row['start_index'] > prevRow['end_index'] or row['end_index'] < prevRow['start_index'])
            subOverlap = (row['phrase'] in prevRow['phrase']) or (prevRow['phrase'] in row['phrase'])
            
            if overlap and subOverlap:
                
                # retain the shorter phrase in case of overlap
                if len(row['phrase']) < len(prevRow['phrase']):
                    indicesDrop.append(prevRow.name)
                else:
                    indicesDrop.append(row.name)

# dropping identified overlapping indices
uniqDrop = list(set(indicesDrop))
dfAlphabetical = dfAlphabetical.drop(uniqDrop).reset_index(drop=True)
dfAlphabetical = dfAlphabetical.drop(0).reset_index(drop=True)
        
# downloading sorted dataset
dataSorted = dfAlphabetical.to_csv()
with open('data1.csv', 'w') as f:
    f.write(dataSorted)
url = 'http://example.com/data.csv'  
response = requests.get(url)
with open('downloaded_data.csv', 'wb') as f:
    f.write(response.content)