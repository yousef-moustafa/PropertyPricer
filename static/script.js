// Create Map
var map = L.map('map').setView([30.0905, 31.6456], 13);


// Define Coordinates
var cairoCoordinates = [
    [31.6092, 30.1075], // North-western point
    [31.6827, 30.1075], // North-eastern point
    [31.6827, 30.0718], // South-eastern point
    [31.6079, 30.0718], // South-western point
    [31.6092, 30.1075]
];

// Create GeoJSON for Cairo Border
var cairoBorder = {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Polygon",
        "coordinates": [cairoCoordinates]
    }
};

// Leaflet layer of the border
L.geoJSON(cairoBorder, {
    style: function (feature) {
        return {
            color: 'orange',
            weight: 5,
            fillColor: 'transparent',
            fillOpacity: 0
        }
    }
}).addTo(map);


L.tileLayer('https://api.maptiler.com/maps/basic-v2-dark/{z}/{x}/{y}.png?key=laxPpdSaC5OByagEhBrp', {
    maxZoom: 19,
    minZoom: 13,
    attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
}).addTo(map);


// Add boundaries to the map (based off cairo borded)
var polygonBounds = L.geoJSON(cairoBorder).getBounds();
map.setMaxBounds(polygonBounds);

// Create Marker
var marker;
var confirmedCoordinates;

function onMapClick(e) {
    if (marker)
    {
        map.removeLayer(marker);
    }
    marker = L.marker(e.latlng).addTo(map);
    const { lat, lng } = e.latlng;

   document.getElementById("latitude").value = lat.toFixed(4);
   document.getElementById("longitude").value = lng.toFixed(4);

    const reverseGeocodingUrl = `https://api.geoapify.com/v1/geocode/reverse?lat=${e.latlng.lat}&lon=${e.latlng.lng}&apiKey=3121046fdc924074a0e0a7bab63314b8`;
    fetch(reverseGeocodingUrl)
    .then(result => result.json())
    .then(featureCollection => {
      if (featureCollection.features.length === 0) {
        console.log("The address is not found");
      }
      const district = featureCollection.features[0].properties.district;
      const address = district !== undefined ? district : "Madinaty";

      // Update the input field with the district information
      document.getElementById("district").value = address;
      // ... (rest of your code)
    })
    .catch(error => {
      console.error("Error fetching address:", error);
    });
}

map.on('click', onMapClick);


// Area value
const areaRange = document.getElementById('area');
const currentArea = document.getElementById('currentArea');

areaRange.addEventListener('input', function() {
    currentArea.textContent = areaRange.value;
})



