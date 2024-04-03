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

def overlapFinder(start, end, df):
    cleanups = []
    for i in range(start, end):
        for j in range(i+1, end):
            phrase1 = df.iloc[i]['phrase']
            phrase2 = df.iloc[j]['phrase']

            if phrase1 in phrase2 or phrase2 in phrase1:
                # Note: Use append(i) or append(j), not append[i] or append[j]
                if len(phrase1) > len(phrase2):
                    cleanups.append(j)  # If phrase1 is longer, mark phrase2 for removal
                else:
                    cleanups.append(i)  # If phrase2 is longer or they are equal, mark phrase1 for removal
    return cleanups

def rowDeleter(indicesDrop, df):
    uniqDrop = list(set(indicesDrop))  # Ensure we have unique indices to drop
    df.drop(uniqDrop, inplace=True)  # Drop rows based on the indices
    df.reset_index(drop=True, inplace=True)  # Reset index after drop
    return df

# Identify groups by context and their start-end indices in the DataFrame
context_groups = dfAlphabetical.groupby('context').apply(lambda x: (x.index[0], x.index[-1] + 1)).tolist()

indicesDrop = []
for start, end in context_groups:
    # Find overlaps within each context group
    overlaps = overlapFinder(start, end, dfAlphabetical)
    indicesDrop.extend(overlaps)

# Delete rows with overlaps
dfCleaned = rowDeleter(indicesDrop, dfAlphabetical)

# grouping by context
grouped = dfCleaned.groupby('context').agg({
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