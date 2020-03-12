//document.addEventListener("load", function(){initialize()});
console.log("Loaded mdfsdfsdfsap");
document.addEventListener("DOMContentLoaded", initialize);

//document.onload = initialize();

function initialize() {
    var mymap = L.map('mapContainer').setView([40, -97], 4);

    var CartoDB_Voyager = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
       attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
       //subdomains: 'abcd', not needed
       maxZoom: 19,
       minZoom: 2,
       noWrap: true
    }).addTo(mymap);

    // Now add the pins from the server
    addPinsToMap(mymap);


    //////////////////////////////////////////////////////////////
         // FeatureGroup is to store editable layers, i.e so they can be removed
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

                layer.bindPopup('Hello world!', {editable: true, nametag: "Something tag", title: "Title"});
            if (type === 'marker') {
               // layer.bindPopup('Hello world!', {editable: true, nametag: "Something tag"});
                // Do marker specific actions
            }
            drawnItems.addLayer(layer);
            // Save to the databse here
            savePinToDatabase(layer);

            // Make a call to ajax to save and hightlight the
            // pin in green then fade the green out (Using css) if the
            // save opperation was successful.  Just an idea.
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

    //////////////////////////////////////////////////////////////////////////
    //////////////////// Overlay loading  ////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////
/*
    var geojsonLayer = new L.GeoJSON.AJAX("http://0.0.0.0:4000/ShapeFileToJSON.geojson", {style: style});
    //geojsonLayer.addTo(mymap);

    //var geojsonLayerE = new L.GeoJSON.AJAX("http://0.0.0.0:8000/gpm_3hr.20200221.235959Europe.geojson", {style: style});
    //geojsonLayerE.addTo(mymap);

    //var geojsonLayerAU = new L.GeoJSON.AJAX("http://0.0.0.0:8000/gpm_3hr.20200221.235959AUS.geojson", {style: style});
    //geojsonLayerAU.addTo(mymap);

    //var geojsonLayerME = new L.GeoJSON.AJAX("http://0.0.0.0:8000/gpm_3hr.20200221.235959ME.geojson", {style: style});
    //geojsonLayerME.addTo(mymap);

    var geojsonLayerGlobe = new L.GeoJSON.AJAX("http://0.0.0.0:4000/gpm_3hr.20200221.235959Globe.geojson", {style: style});
*/
    //These make the map run slow, they contain too much data
    //var CurWarningjsonLayerGlobe = new L.GeoJSON.AJAX("http://0.0.0.0:8000/CurrentWarnings.geojson", {style: WarningStyle});

    //var FireWarningjsonLayerGlobe = new L.GeoJSON.AJAX("http://0.0.0.0:8000/FireData.geojson", {style: WarningStyle});

    // For the top right button, can add more here
  /*  var overlayMaps = {
        "America Rain": geojsonLayer,
        "Global Rain":geojsonLayerGlobe,
    }*/

        //"Current Warnings":CurWarningjsonLayerGlobe
        //"Fire Warnings": FireWarningjsonLayerGlobe
            //"Europe Rain": geojsonLayerE,
        //"Austrailian Rain": geojsonLayerAU,
        //"Middle East Rain": geojsonLayerME,

        // This adds the actual overlay top right button to the map
        //L.control.layers(null, overlayMaps).addTo(mymap);


        /////////////////////////////////////////////////////////////////////////////////////

        csrftoken = getCookie('csrftoken');
        }

// See https://docs.djangoproject.com/en/dev/ref/csrf/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken;
// //////////////////////////////

function savePinToDatabase(layer){

//console.log(layer)

  $.ajax({
      type: 'POST',
      beforeSend: function(request) {
      request.setRequestHeader("X-CSRFToken", csrftoken);
      },
      url: 'WeatherSTUFF/add_pin/', // this handles the post data //WeatherSTUFF WeatherSTUFF/about/
      dataType: 'json',
      data: {
                'lat':layer['_latlng']['lat'],
                'lng': layer['_latlng']['lng'],
                'content': layer['_popup']['_content'] ,//"Hello",//layer, // Pin data
                'title': 'Not Yet Implimented',
                'date': '',//Date().toLocaleString(),
                'csrfmiddlewaretoken': String(csrftoken),
             },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        layer.remove();
        //console.log(XMLHttpRequest);
        if(XMLHttpRequest.status == "401"){
          //console.log(XMLHttpRequest)
          //User profile not authenticated
          alert("Error "+XMLHttpRequest.status+" : "+XMLHttpRequest.responseText);
        }
        //console.log("Status: " + XMLHttpRequest.status); console.log("Error: " + errorThrown);
      },
      //success: return true,
  });
}

function addPinsToMap(map){

  var prevPins = new L.FeatureGroup();
  map.addLayer(prevPins);

  $.get("WeatherSTUFF/get_pins/", function(data, status){
    // loop through each pin and add each to the map
    //console.log("Data: " + data + "\nStatus: " + status);

    for(m in data){
      var mf = data[m]["fields"];

      var myMarker =  L.marker( [mf["x_val"], mf["y_val"]] );
      console.log(mf['title']);
      myMarker.bindPopup( mf["content"] , {editable: true, title:mf['title']} )//.addTo(map)
      prevPins.addLayer(myMarker);
    }
});
}
