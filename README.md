Practice cleaning unorganised data and converting to json in a specified format:

Convert data provided to this json format:

{ “context”: <context-text>,

“entities”:[(entitity_1, start_index1, end_index1), (entity_2, start_index2, end_index2)……,

“phrase”: [(phrase1),(phrase2),(phrase3)...] }

Challenges are:

1. context should not be repeated in data, if data have same context merge it and sperated out entities as above format
2. for the same context data the phrase should be unique and no two phrase should overlap

When handling overlap:  take which makes more sense, you might need to explore data initially

also you cannot chop the word →

context: i love being australian

phrase shouldnot be “australia” as this is chopping the word

it gets interesting when phrases are 2+ words

also there might be spelling issues and those kinda of things as well