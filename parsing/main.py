import json

with open('all_urls.json', 'r') as json_file:
    urls_d = json.load(json_file)

links = [obj['Address'] for obj in urls_d]

print(links)

 