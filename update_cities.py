import json

with open('app/data/cities.json', 'r') as f:
    cities = json.load(f)

for city in cities:
    if city['id'] == 'kld':
        city['id'] = 'guryevsk'
        city['name'] = 'г. Гурьевск'
        city['coordinates'] = [20.6037, 54.7745]
    elif city['id'] == 'adg':
        city['id'] = 'yablonovsky'
        city['name'] = 'пгт. Яблоновский'
        city['coordinates'] = [38.9382, 44.9864]
    elif city['id'] == 'krd':
        city['id'] = 'krasnodar'
        # krasnodar is already correct
        
with open('app/data/cities.json', 'w') as f:
    json.dump(cities, f, ensure_ascii=False, indent=2)
