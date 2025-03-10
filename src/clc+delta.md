```js
import {loadDepartmentGeom, loadDepartmentLevel, loadDepartmentEvol} from "./components/loaders.js";
import {getConfig} from "./components/config.js";
import {transformData} from "./components/build-table.js";
import {getCentroid} from "./utils/fonctions.js";
import {getOSM, getOSMDark, getMarker, getSatelliteImages, getPredictions, getClusters, getEvolutions} from "./components/map-layers.js";
import {filterObject} from "./components/utils.js";
```

```js
// Crée un élément h1 avec le nom du département
const titre = html`<h1>CLC+ Delta</h1>`;
display(titre);
```


```js
const nuts3 = FileAttachment("./data/nuts3.json").json()
const statNuts3 = FileAttachment('./data/statNuts3.parquet').parquet()
const available_years = ['2018','2021','2024']
```


```js
//récupération du centre de l'ilot à partir de l'ilot sélectionné
const placeholder_nuts = "BE251"
const placeholder_name = "Bruxelles"
const placeholder_nuts_name = placeholder_nuts + " " + placeholder_name

const search = view(
     Inputs.search(statNuts3, 
     {
       placeholder: placeholder_nuts_name,
       columns:["NUTS3","name"]
     })
   )
```
```js
const search_table = view(
      Inputs.table(search, {
        columns: ['NUTS3','name','artificial_ratio_2018', 'artificial_ratio_2021', 'artificial_ratio_evolution'],
        header: {
          NUTS3: 'NUTS3',
          name: 'Name',
          artificial_ratio_2018: 'Art. Ratio 2018 (%)',
          artificial_ratio_2021: 'Art. Ratio 2021 (%)',
          artificial_ratio_evolution: 'Art. Ratio Evolution (%)'
        },
        width: {
          NUTS3: 120,
          Name: 120,
          artificial_ratio_2018: 150,
          artificial_ratio_2021: 150,
          artificial_ratio_evolution: 180
        },
        format: {
          artificial_ratio_2018: x => `${(Math.round(x * 10) / 10).toFixed(1)}%`,
          artificial_ratio_2021: x => `${(Math.round(x * 10) / 10).toFixed(1)}%`,
          artificial_ratio_evolution: x => `${(Math.round(x * 10) / 10).toFixed(1)}%`
        },
        sort: {
          column: 'NUTS3',
          reverse: false
        },
        rows: 10
      })
    );
```
```js
const center = getCentroid(
    nuts3,
    search[0]?.NUTS3||placeholder_nuts ,
  )
```


```js
// Initialisation de la carte Leaflet
const mapDiv = display(document.createElement("div"));
mapDiv.style = "height: 600px; width: 100%; margin: 0 auto;";

// Initialiser la carte avec la position centrale du département
const map = L.map(mapDiv, {
            center: center,
            zoom: 10,           
            maxZoom: 21 //(or even higher)
        });

// Adding the WMS layer
const CLCplus2018 = L.tileLayer.wms("https://copernicus.discomap.eea.europa.eu/arcgis/services/CLC_plus/CLMS_CLCplus_RASTER_2018_010m_eu/ImageServer/WMSServer?", {
    layers: "CLMS_CLCplus_RASTER_2018_010m_eu",
    format: "image/png",
    transparent: true,
    version: "1.3.0",
    opacity: 0.5, 
    attribution: "© Copernicus CLC+ 2018 - European Environment Agency"
});

const CLCplus2021 = L.tileLayer.wms("https://copernicus.discomap.eea.europa.eu/arcgis/services/CLC_plus/CLMS_CLCplus_RASTER_2021_010m_eu/ImageServer/WMSServer?", {
    layers: "CLMS_CLCplus_RASTER_2021_010m_eu",
    format: "image/png",
    transparent: true,
    version: "1.3.0",
    opacity: 0.5, 
    attribution: "© Copernicus CLC+ 2021 - European Environment Agency"
});
// Add WMS layer to map

// Add WMS layer for CLC+ 2021 with Invert filter
const InvertCLC = L.tileLayer.wms("https://copernicus.discomap.eea.europa.eu/arcgis/services/CLC_plus/CLMS_CLCplus_RASTER_2021_010m_eu/ImageServer/WMSServer?", {
    layers: "CLMS_CLCplus_RASTER_2021_010m_eu",
    format: "image/png",
    transparent: true,
    version: "1.3.0",
    opacity: 0.35,
    attribution: "© Copernicus CLC+ 2021 - European Environment Agency"
});

InvertCLC.on('tileload', function(event) {
    const tile = event.tile;
    // Apply the invert CSS filter to the tile image
    tile.style.filter = 'invert(1)';
});

// Ajout d'une couche de base OpenStreetMap
const OSM = getOSM();
const OSMDark  = getOSMDark();
const marker = getMarker(center);
const BORDERS = getClusters(nuts3);

const Sentinel2 = getSatelliteImages();
const selectedSentinel2 = filterObject(Sentinel2, [`Sentinel2 2018`, `Sentinel2 2021`, `Sentinel2 2024`])


OSM['OpenStreetMap clair'].addTo(map);
BORDERS["nuts boundaries"].addTo(map);


const urlGeoServer = "https://geoserver-hachathon2025.lab.sspcloud.fr/geoserver/hachathon2025/wms";
const workSpace = "hachathon2025";

const differences = L.tileLayer.wms(urlGeoServer, {
    layers: `${workSpace}:change_polygons_CLC`,
    format: 'image/png',
    transparent: true,
    version: '1.1.0',
    opacity: 1,
    maxZoom: 21,
    styles : "style_multiclass",
   // CQL_FILTER: "INCLUDE",
  //  cql_filter: `class='3'`  
});

marker.addTo(map);
```


```js

const predictions = L.tileLayer.wms("https://geoserver-hachathon2025.lab.sspcloud.fr/geoserver/hachathon2025/wms", {
            layers: "hachathon2025:predUE2024",  // Layer name
            format: 'image/png',  // Use image format
            transparent: true,  // Keep background transparent
            version: '1.1.0',  // WMS version
            attribution: "GeoServer Hachathon 2025",
           // cql_filter: `label='1'`
        });


```


```js
 L.control.layers({
   ...OSM,
   ...OSMDark,  
   },
{ ...selectedSentinel2,
 [`CLC+ 2018`]: CLCplus2018,
  [`CLC+ 2021`]: CLCplus2021,
  [`Inverted CLC+ 2021`]: InvertCLC,
}
).addTo(map);

```