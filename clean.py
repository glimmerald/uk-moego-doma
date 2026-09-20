import json

def get_area(coords):
    area = 0.0
    for i in range(len(coords) - 1):
        area += coords[i][0] * coords[i+1][1] - coords[i+1][0] * coords[i][1]
    return abs(area) / 2.0

with open('app/public/krasnodar.geojson', 'r') as f:
    geom = json.load(f)

if geom['type'] == 'MultiPolygon':
    largest_poly = None
    max_area = -1
    for poly in geom['coordinates']:
        area = get_area(poly[0])
        if area > max_area:
            max_area = area
            largest_poly = poly
    
    clean_geom = {
        'type': 'Polygon',
        'coordinates': [largest_poly[0]]
    }
elif geom['type'] == 'Polygon':
    clean_geom = {
        'type': 'Polygon',
        'coordinates': [geom['coordinates'][0]]
    }

feature_collection = {
    'type': 'FeatureCollection',
    'features': [{
        'type': 'Feature',
        'properties': {'admin': 'Krasnodar'},
        'geometry': clean_geom
    }]
}

with open('app/public/krasnodar.geojson', 'w') as f:
    json.dump(feature_collection, f)

print("Cleaned!")
