import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const citiesPath = path.resolve(__dirname, '../data/cities.json');
const MAPBOX_TOKEN = 'pk.eyJ1Ijoiamsta3Jhc25vZGFyIiwiYSI6ImNtdThhdzYwbzBxMWEyeXM3ZDNnNGJoOTkifQ.kqIYZO0xU7inIoXFKFjpWQ';

const cities = JSON.parse(fs.readFileSync(citiesPath, 'utf8'));

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function geocodeAddress(query, proximity) {
  const url = new URL(`https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(query)}.json`);
  url.searchParams.set('access_token', MAPBOX_TOKEN);
  url.searchParams.set('country', 'ru');
  url.searchParams.set('language', 'ru');
  url.searchParams.set('limit', '1');
  if (proximity && proximity.length === 2) {
    url.searchParams.set('proximity', `${proximity[0]},${proximity[1]}`);
  }

  const response = await fetch(url.toString());
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const data = await response.json();
  if (data.features && data.features.length > 0) {
    const feature = data.features[0];
    return {
      center: feature.center, // [lng, lat]
      place_name: feature.place_name,
      relevance: feature.relevance
    };
  }
  return null;
}

async function run() {
  console.log('--- Starting Mapbox Geocoding for all complexes ---');
  let updatedCount = 0;
  let totalCount = 0;

  for (const city of cities) {
    console.log(`\nCity: ${city.name} (${city.id})`);
    for (const complex of city.complexes) {
      totalCount++;
      const fullAddress = `${city.name}, ${complex.address}`;
      try {
        const result = await geocodeAddress(fullAddress, city.coordinates);
        if (result && result.center) {
          const newCoords = [
            Number(result.center[0].toFixed(6)),
            Number(result.center[1].toFixed(6))
          ];
          const oldCoords = complex.coordinates;
          console.log(`  ✓ [${complex.name}] (${complex.address})`);
          console.log(`    Old: [${oldCoords.join(', ')}] -> New: [${newCoords.join(', ')}]`);
          console.log(`    Found: "${result.place_name}" (relevance: ${result.relevance})`);
          complex.coordinates = newCoords;
          updatedCount++;
        } else {
          console.warn(`  ✗ [${complex.name}] (${fullAddress}) - Not found via Mapbox Geocoder, keeping old coords: [${complex.coordinates.join(', ')}]`);
        }
      } catch (err) {
        console.error(`  ! Error geocoding [${complex.name}]:`, err.message);
      }
      await sleep(200); // 200ms delay between API requests
    }
  }

  fs.writeFileSync(citiesPath, JSON.stringify(cities, null, 2) + '\n', 'utf8');
  console.log(`\n--- Completed: successfully geocoded ${updatedCount} of ${totalCount} complexes. Saved to ${citiesPath} ---`);
}

run();
