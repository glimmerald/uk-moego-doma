import json

def polygon_area(coords):
    area = 0.0
    for i in range(len(coords)):
        j = (i + 1) % len(coords)
        area += coords[i][0] * coords[j][1]
        area -= coords[j][0] * coords[i][1]
    return abs(area) / 2.0

def process(infile, outfile):
    with open(infile, 'r') as f:
        data = json.load(f)

    if data['type'] == 'GeometryCollection':
        polygons = [g for g in data['geometries'] if g['type'] in ('Polygon', 'MultiPolygon')]
    elif data['type'] in ('Polygon', 'MultiPolygon'):
        polygons = [data]
    elif data['type'] == 'FeatureCollection':
        polygons = [f['geometry'] for f in data['features'] if f['geometry']['type'] in ('Polygon', 'MultiPolygon')]
    else:
        polygons = [data] # Fallback

    if not polygons:
        print(f"No polygons found in {infile}")
        return

    best_poly = None
    max_area = -1

    for geom in polygons:
        if geom['type'] == 'Polygon':
            coords = geom['coordinates'][0]
            area = polygon_area(coords)
            if area > max_area:
                max_area = area
                best_poly = coords
        elif geom['type'] == 'MultiPolygon':
            for poly in geom['coordinates']:
                coords = poly[0]
                area = polygon_area(coords)
                if area > max_area:
                    max_area = area
                    best_poly = coords

    out_geom = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [best_poly]
                }
            }
        ]
    }

    with open(outfile, 'w') as f:
        json.dump(out_geom, f)
    print(f"Processed {infile} -> {outfile}")

process('guryevsk_raw.geojson', 'app/public/guryevsk.geojson')
process('yablonovsky_raw.geojson', 'app/public/yablonovsky.geojson')
