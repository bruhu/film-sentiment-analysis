# Extract category names out of category codes from the responses in doesthedogdie.com


import json


with open('./data/doesthedog_response.json', 'r') as file:
    data = json.load(file)

categories_dict = {}

if isinstance(data.get('topicItemStats'), list):
    # Iterate over the list of topic items
    for item in data['topicItemStats']:
        # Check if 'topic' is present in the current item and is a dictionary
        if isinstance(item.get('topic'), dict):
            topic = item['topic']
            # Extract 'id' and 'smmwDescription' (or other fields)
            category = topic.get('id')
            event = topic.get('smmwDescription')
            
            # Store the values in the dictionary
            if category is not None and event is not None:
                categories_dict[category] = event
                print(f'Category: {category}, Event: {event}')
        else:
            print(f'Topic is not a dictionary in item {item.get('topicItemId')}')
else:
    print('topicItemStats is not a list.')

print(categories_dict)


