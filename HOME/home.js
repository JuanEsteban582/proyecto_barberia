require([
  "esri/config", 
  "esri/Map", 
  "esri/views/MapView", 
  "esri/Graphic",
  "esri/layers/GraphicsLayer",
  "esri/rest/route",
  "esri/rest/support/RouteParameters",
  "esri/rest/support/FeatureSet"
 ], function(esriConfig, Map, MapView, Graphic, GraphicsLayer, route, RouteParameters, FeatureSet) {
   
  esriConfig.apiKey = "AAPKa694a97d95ff4ddcad5e8c63e4e979b6WgwfJTWIkkV759NWar8NAbyCtUKtnjsohR1_MUr2BnxhTOIzOF9RiroKPkm_xNyP";
   
  const map = new Map({
       basemap: "arcgis-navigation"
  });
   
  const view = new MapView({
       container: "viewDiv",
       map: map,
       center: [-76.29783, 3.90089], 
       zoom: 13
  });
   
  const graphicsLayer = new GraphicsLayer();
  map.add(graphicsLayer);
   
  function obtenerUbicacionYMostrar() {
       if (navigator.geolocation) {
         navigator.geolocation.getCurrentPosition(function(position) {
           const lat = position.coords.latitude;
           const lon = position.coords.longitude;
   
           document.getElementById("locationDisplay").innerText = `Ubicación actual: ${lat.toFixed(6)}, ${lon.toFixed(6)}`;
   
           const userPoint = {
             type: "point",
             longitude: lon,
             latitude: lat
           };
   
           const userGraphic = new Graphic({
            geometry: userPoint,
            symbol: {
               type: "simple-marker",
               color: [213, 80, 37], 
               outline: {
                 color: [46, 37, 24], 
                 width: 1
               }
            },
            popupTemplate: {
               title: "Tu Estas aqui",
               content: "Aquí está tu ubicación actual."
            }
           });
   
           graphicsLayer.add(userGraphic);
   
           view.goTo({
             target: [lon, lat],
             zoom: 15
           });
   
          
           calcularRutaBarberia(lon, lat);
         }, function(error) {
           console.error("Error al obtener la ubicación: " + error.message);
         });
       } else {
         console.error("Geolocalización no es soportada por este navegador.");
       }
  }
   
  function calcularRutaBarberia(userLon, userLat) {
       const barberiaLat = 3.9126708;
       const barberiaLon = -76.2983755;
   
       
       const barberiaPoint = {
           type: "point",
           longitude: barberiaLon,
           latitude: barberiaLat
       };
   
       const barberiaMarkerSymbol = {
           type: "simple-marker",
           color: [255, 0, 0], // Color rojo
           outline: {
               color: [46, 37, 24], // White
               width: 1
           }
       };
   
       const barberiaGraphic = new Graphic({
           geometry: barberiaPoint,
           symbol: barberiaMarkerSymbol,
           attributes: {
               name: "Barbería"
           },
           popupTemplate: {
               title: "Barbería",
               content: "Aquí está la barbería."
           }
       });
   
       graphicsLayer.add(barberiaGraphic);
   
       const routeUrl = "https://route-api.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World";
   
       const routeParams = new RouteParameters({
         stops: new FeatureSet({
           features: [
             new Graphic({
               geometry: {
                 type: "point",
                 longitude: userLon,
                 latitude: userLat
               }
             }),
             barberiaGraphic // Agregar el marcador de la barbería como parada
           ]
         }),
         returnDirections: true,
         directionsLanguage: "es"
       });
   
       route.solve(routeUrl, routeParams)
         .then((data) => {
           if (data.routeResults.length > 0) {
             showRoute(data.routeResults[0].route);
             showDirections(data.routeResults[0].directions.features);
           }
         })
         .catch((error) => {
           console.error("Error al calcular la ruta:", error);
         });
  }
   
  function showRoute(routeResult) {
       routeResult.symbol = {
         type: "simple-line",
         color: [5, 150, 255],
         width: 3
       };
       view.graphics.add(routeResult, 0);
  }
   
  function showDirections(directions) {
       const directionsElement = document.createElement("div");
       directionsElement.innerHTML = "<h3>Direcciones</h3>";
       directionsElement.classList = "esri-widget esri-widget--panel esri-directions__scroller directions";
       directionsElement.style.marginTop = "0";
       directionsElement.style.padding = "0 15px";
       directionsElement.style.minHeight = "365px";
   
       const directionsList = document.createElement("ol");
       directions.forEach(function(result) {
         const direction = document.createElement("li");
         direction.innerHTML = result.attributes.text + ((result.attributes.length > 0) ? " (" + result.attributes.length.toFixed(2) + " km)" : "");
         directionsList.appendChild(direction);
       });
       directionsElement.appendChild(directionsList);
   
       view.ui.empty("top-right");
       view.ui.add(directionsElement, "top-right");
  }
   
  obtenerUbicacionYMostrar();
 });