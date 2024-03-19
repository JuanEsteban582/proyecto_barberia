window.onload = function() {
    require([
      "esri/config", 
      "esri/Map", 
      "esri/views/MapView", 
      "esri/intl", 
      "esri/Graphic",
      "esri/layers/GraphicsLayer",
      "esri/widgets/Locate",
      "esri/widgets/Search"
    
      ], function(esriConfig, Map, MapView, intl, Graphic, GraphicsLayer, Locate, Search) {

      esriConfig.apiKey = "AAPKa694a97d95ff4ddcad5e8c63e4e979b6WgwfJTWIkkV759NWar8NAbyCtUKtnjsohR1_MUr2BnxhTOIzOF9RiroKPkm_xNyP";

        intl.setLocale("es");

        const map = new Map({
          basemap: {
            style: {
                id: "arcgis/outdoor",
                language: "es"
            }
          }   // basemap styles service
        });

        const view = new MapView({
          map: map,
          center: [-76.29783, 3.90089], // Longitude, latitude
          zoom: 13, // Zoom level
          container: "viewDiv" // Div element
        });

        const search = new Search({
          view: view
        });

        const locateBtn = new Locate({
          view: view
        });

        view.ui.add(search, "top-right");

        view.ui.add(locateBtn, {
          position: "top-left"
        });

        const graphicsLayer = new GraphicsLayer();
        map.add(graphicsLayer);

        const point = { //Create a point
          type: "point",
          longitude: -76.29854,
          latitude: 3.91334
        };

        const simpleMarkerSymbol = {
          type: "simple-marker",
          color: [213, 80, 37],  // Orange
          outline: {
              color: [46, 37, 24], // White
              width: 1
          }
        };

        const popupTemplate = {
          title: "{Name}",
          content: "<img style='width: 100px;' src='{Image}'>"
        }

        const attributes = {
          Name: "Barbería Door Of Juda",
          Description: "La mejor barberia",
          Image: "https://img.freepik.com/vector-premium/vintage-barberia-vector-logo-plantilla-etiqueta_278810-684.jpg?size=338&ext=jpg&ga=GA1.1.87170709.1707091200&semt=ais",
        }

        const pointGraphic = new Graphic({
            geometry: point,
            symbol: simpleMarkerSymbol,

            attributes: attributes,
            popupTemplate: popupTemplate
        });
        graphicsLayer.add(pointGraphic);

        
    });

  }

