
function initialize() {

//var mymap = L.map('mapContainer').setView([51.505, -0.09], 13); //.setView([51.505, -0.09], 13);

var mymap = L.map('mapContainer').setView([40, -97], 13);

var CartoDB_Voyager = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
   attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
   //subdomains: 'abcd',
   maxZoom: 19,
   minZoom: 2, 
   noWrap: true
}).addTo(mymap);


//////////////////////////////////////////////////////////////
     // FeatureGroup is to store editable layers
     var drawnItems = new L.FeatureGroup();
     mymap.addLayer(drawnItems);
     var drawControl = new L.Control.Draw({
         edit: {
             featureGroup: drawnItems
         }
     });
     mymap.addControl(drawControl);

     mymap.on(L.Draw.Event.CREATED, function (e) {
        var type = e.layerType,
            layer = e.layer;
            layer.bindPopup('Hello world!', {editable: true, nametag: "Something tag"});
        if (type === 'marker') {
           // layer.bindPopup('Hello world!', {editable: true, nametag: "Something tag"});
            // Do marker specific actions
        }
        drawnItems.addLayer(layer);
        // Do whatever else you need to. (save to db; add to map etc)
        //mymap.addLayer(layer);
     });

     var fireStyle = {
        "color": "#ffa500",
        "weight": 5,
        "opacity": 1
    };

     var geojsonFeature =  {
         "type":"FeatureCollection","features":
         [{"type":"Feature","properties":{"DN":0,"VALID":"202002291200","EXPIRE":"202003011200"},
         "geometry":{"type":"Polygon","coordinates":[[[-5424906.935892342,6885651.525545033],[-5426673.926526984,6881503.859357518],[-5426373.889554942,6884146.120704022],[-5424906.935892342,6885651.525545033]]]}}]}
     
         L.geoJSON(geojsonFeature, {
        style: fireStyle
    }).addTo(mymap);


   function getColor(d) {
    return d > 1000 ? '#800026' :
           d > 500  ? '#BD0026' :
           d > 200  ? '#E31A1C' :
           d > 100  ? '#FC4E2A' :
           d > 50   ? '#FD8D3C' :
           d > 20   ? '#FEB24C' :
           d > 10   ? '#FED976' :
                      '#FFEDA0';
}

   function styleS(feature) {
    return {
        fillColor: '#800026',
        weight: 0.1,
        opacity: 0.00,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.00001
    };
}

var style = {
    "clickable": true,
    "color": "#00D",
    "fillColor": "#00D",
    "weight": 0.0,
    "opacity": 0.3,
    "fillOpacity": 0.1
};


var WarningStyle = {
    "clickable": true,
    "color": "#FF7F00",
    "fillColor": "#FF7F00",
    "weight": 0.0,
    "opacity": 0.3,
    "fillOpacity": 0.1
};


var hoverStyle = {
    "fillOpacity": 0.5
};

var geojsonLayer = new L.GeoJSON.AJAX("http://0.0.0.0:4000/ShapeFileToJSON.geojson", {style: style});
//geojsonLayer.addTo(mymap);

//var geojsonLayerE = new L.GeoJSON.AJAX("http://0.0.0.0:8000/gpm_3hr.20200221.235959Europe.geojson", {style: style});
//geojsonLayerE.addTo(mymap);

//var geojsonLayerAU = new L.GeoJSON.AJAX("http://0.0.0.0:8000/gpm_3hr.20200221.235959AUS.geojson", {style: style});
//geojsonLayerAU.addTo(mymap);

//var geojsonLayerME = new L.GeoJSON.AJAX("http://0.0.0.0:8000/gpm_3hr.20200221.235959ME.geojson", {style: style});
//geojsonLayerME.addTo(mymap);

var geojsonLayerGlobe = new L.GeoJSON.AJAX("http://0.0.0.0:4000/gpm_3hr.20200221.235959Globe.geojson", {style: style});

//These make the map run slow, they contain too much data
//var CurWarningjsonLayerGlobe = new L.GeoJSON.AJAX("http://0.0.0.0:8000/CurrentWarnings.geojson", {style: WarningStyle});

//var FireWarningjsonLayerGlobe = new L.GeoJSON.AJAX("http://0.0.0.0:8000/FireData.geojson", {style: WarningStyle});

// For the top right button, can add more here
var overlayMaps = {
    "America Rain": geojsonLayer,
    "Global Rain":geojsonLayerGlobe,    
}

    //"Current Warnings":CurWarningjsonLayerGlobe
    //"Fire Warnings": FireWarningjsonLayerGlobe
        //"Europe Rain": geojsonLayerE,
    //"Austrailian Rain": geojsonLayerAU,
    //"Middle East Rain": geojsonLayerME,

    // This adds the actual overlay top right button to the map
    L.control.layers(null, overlayMaps).addTo(mymap);

    }
