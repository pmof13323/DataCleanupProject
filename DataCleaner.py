import pandas as pd
import requests
import json

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
                    indicesDrop.append(row.name)
                else:
                    indicesDrop.append(prevRow.name)

# dropping identified overlapping indices
uniqDrop = list(set(indicesDrop))
dfAlphabetical = dfAlphabetical.drop(uniqDrop).reset_index(drop=True)
dfAlphabetical = dfAlphabetical.drop(0).reset_index(drop=True)

# grouping by context
grouped = dfAlphabetical.groupby('context').agg({
    'type': lambda x: list(x),
    'start_index': lambda x: list(x),
    'end_index': lambda x: list(x),
    'phrase': lambda x: list(x)
}).reset_index()

# create JSON objects
jsonList = []
for index, row in grouped.iterrows():
    context = row['context']
    entities = list(zip(row['type'], row['start_index'], row['end_index']))
    phrases = row['phrase']
    jsonObj = {
        "context": context,
        "entities": entities,
        "phrase": phrases
    }
    jsonList.append(jsonObj)

# convert to JSON string
jsonOutput = json.dumps(jsonList, indent=4)

# write to file
with open('output.json', 'w') as f:
    f.write(jsonOutput)