const https = require('https');
const fs = require('fs');

const options = {
  hostname: 'nominatim.openstreetmap.org',
  path: '/search?city=Krasnodar&country=Russia&format=json&polygon_geojson=1',
  headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0' }
};

https.get(options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const json = JSON.parse(data);
    const geojson = {
      type: 'FeatureCollection',
      features: [{ type: 'Feature', properties: { admin: 'Krasnodar' }, geometry: json[0].geojson }]
    };
    fs.writeFileSync('app/public/krasnodar.geojson', JSON.stringify(geojson));
    console.log('Saved to app/public/krasnodar.geojson');
  });
});
