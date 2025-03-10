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
const titre = html`<h1>Predictions</h1>`;
display(titre);
```


```js
const nuts3 = FileAttachment("./data/nuts3.json").json()
const statNuts3 = FileAttachment('./data/proportionNuts3.parquet').parquet()
const statsPlot = FileAttachment('./data/statsPopulationNuts3.parquet').parquet()
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
        columns: ["NUTS3","name","artificial_ratio_2018", "artificial_ratio_2021", "artificial_ratio_2024", "artificial_evolution_2018_2024","artificial_evolution_2021_2024"],
        header: {
          NUTS3: 'NUTS3',
          name: 'Name',
          artificial_ratio_2018: 'Art. R. 2018',
          artificial_ratio_2021: 'Art. R. 2021',
          artificial_ratio_2024: 'Art. R. 2024',
          artificial_evolution_2018_2024: 'Evol 2018-2024',
          artificial_evolution_2021_2024: 'Evol 2021-2024'
        },
        width: {
          NUTS3: 80,
          name: 120,
          artificial_ratio_2018: 100,
          artificial_ratio_2021: 100,
          artificial_ratio_2024: 100,
          artificial_evolution_2018_2024: 110,
          artificial_evolution_2021_2024: 110
        },
        format: {
          artificial_ratio_2018: x => `${(Math.round(x * 10) / 10).toFixed(1)}%`,
          artificial_ratio_2021: x => `${(Math.round(x * 10) / 10).toFixed(1)}%`,
          artificial_ratio_2024: x => `${(Math.round(x * 10) / 10).toFixed(1)}%`,
          artificial_evolution_2018_2024: x => `${(Math.round(x * 10) / 10).toFixed(1)}%`,
          artificial_evolution_2021_2024: x => `${(Math.round(x * 10) / 10).toFixed(1)}%`
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

const predictions_2018 = L.tileLayer.wms("https://geoserver-hachathon2025.lab.sspcloud.fr/geoserver/hachathon2025/wms", {
            layers: "hachathon2025:predUE2018",  // Layer name
            format: 'image/png',  // Use image format
            transparent: true,  // Keep background transparent
            version: '1.1.0',  // WMS version
            attribution: "GeoServer Hachathon 2025",
           // cql_filter: `label='1'`
        });


const predictions_2021 = L.tileLayer.wms("https://geoserver-hachathon2025.lab.sspcloud.fr/geoserver/hachathon2025/wms", {
            layers: "hachathon2025:predUE2021",  // Layer name
            format: 'image/png',  // Use image format
            transparent: true,  // Keep background transparent
            version: '1.1.0',  // WMS version
            attribution: "GeoServer Hachathon 2025",
           // cql_filter: `label='1'`
        });


const predictions_2024 = L.tileLayer.wms("https://geoserver-hachathon2025.lab.sspcloud.fr/geoserver/hachathon2025/wms", {
            layers: "hachathon2025:predUE2024",  // Layer name
            format: 'image/png',  // Use image format
            transparent: true,  // Keep background transparent
            version: '1.1.0',  // WMS version
            attribution: "GeoServer Hachathon 2025",
           // cql_filter: `label='1'`
        });

```

```js

////////////////////////////////////////////
// 1) Définition de la légende
////////////////////////////////////////////

// Tableau des classes de la couche "predictions" (exemple)
// Tableau des classes et couleurs (vous pouvez adapter les couleurs exactes)
const predictionsClasses = [
  { label: "Sealed (1)", color: "#FF0100" },
  { label: "Woody – needle leaved trees (2)", color: "#238B23" },
  { label: "Woody – Broadleaved deciduous trees (3)", color: "#80FF00" },
  { label: "Woody – Broadleaved evergreen trees (4)", color: "#00FF00" },
  { label: "Low-growing woody plants (bushes, shrubs) (5)", color: "#804000" },
  { label: "Permanent herbaceous (6)", color: "#CCF24E" },
  { label: "Periodically herbaceous (7)", color: "#FEFF80" },
  { label: "Lichens and mosses (8)", color: "#FF81FF" },
  { label: "Non- and sparsely-vegetated (9)", color: "#BFBFBF" },
  { label: "Water (10)", color: "#0080FF" }
];

// Création d’un contrôle Leaflet (position : bottomright)
const predictionsLegend = L.control({ position: 'bottomright' });

predictionsLegend.onAdd = function (map) {
  // Conteneur principal <div>
  const div = L.DomUtil.create("div", "info legend");

  // Rendez le fond blanc/transparent, le texte noir, etc.
  // Vous pouvez ajuster l’opacité, la couleur de la bordure, etc.
  div.style.background = "rgba(255, 255, 255, 0.8)";
  div.style.padding = "8px";
  div.style.borderRadius = "6px";
  div.style.border = "1px solid #999";
  div.style.color = "#000";

  // Un titre en haut de la légende
  div.innerHTML += "<h4 style='margin-top:0; color: black;'>Predictions</h4>";

  // Pour chaque classe : un petit carré coloré + le label
  predictionsClasses.forEach((c) => {
    div.innerHTML += `
      <div style="display: flex; align-items: center; margin-bottom: 4px; font-size: 14px;">
        <!-- Carré de couleur -->
        <span style="
          width: 18px;
          height: 18px;
          background: ${c.color};
          display: inline-block;
          margin-right: 8px;
          border: 1px solid #999;">
        </span>
        <span>${c.label}</span>
      </div>
    `;
  });

  return div;
};

////////////////////////////////////////////
// 2) Gestion de l’affichage conditionnel
////////////////////////////////////////////

// Écoute l'événement "overlayadd": activé lorsqu'un overlay est coché dans la liste
map.on("overlayadd", function(e) {
  // e.name correspond au libellé de la couche dans le control.layers
  // ou e.layer est la couche en question.
  //
  // Si le nom correspond à "predictions" (celui que vous avez dans le control.layers),
  // alors on ajoute la légende sur la carte.
  if (e.name === "Pred 2018" || e.name === "Pred 2021" || e.name === "Pred 2024") {
    predictionsLegend.addTo(map);
  }
});

// Écoute l'événement "overlayremove": déclenché lorsqu'un overlay est décoché
map.on("overlayremove", function(e) {
  if (e.name === "Pred 2018" || e.name === "Pred 2021" || e.name === "Pred 2024") {
    map.removeControl(predictionsLegend);
  }
});
```
```js 
const imperviousBuilt = L.tileLayer.wms("https://image.discomap.eea.europa.eu/arcgis/services/GioLandPublic/HRL_BuiltUp_2018/ImageServer/WMSServer?", {
    layers: "HRL_BuiltUp_2018", // You may need to check the exact layer name in the GetCapabilities response
    format: 'image/png',
    transparent: true,
    version: '1.3.0',
    attribution: "© Copernicus HRL Built-Up 2018 - European Environment Agency",
    opacity: 0.7
});

// Create a new WMS layer for HRL Forest Type 2018
const layerForest = L.tileLayer.wms("https://image.discomap.eea.europa.eu/arcgis/services/GioLandPublic/HRL_ForestType_2018/ImageServer/WMSServer?", {
    layers: "HRL_ForestType_2018", // Ensure this is the correct layer name from GetCapabilities
    format: 'image/png',
    transparent: true,
    version: '1.3.0',
    attribution: "© Copernicus HRL Forest Type 2018 - European Environment Agency",
    opacity: 0.7
});

```
```js
 L.control.layers({
   ...OSM,
   ...OSMDark,  
   },
{ ...selectedSentinel2,
 [`Pred 2018`]: predictions_2018,
  [`Pred 2021`]: predictions_2021,
 [`Pred 2024`]:  predictions_2024,
 [`CLC+ 2018`]: CLCplus2018,
  [`CLC+ 2021`]: CLCplus2021,
  [`Inverted CLC+ 2021`]: InvertCLC,
  [`imperviousBuilt`]:imperviousBuilt,
  [`Forest`]: layerForest
}
).addTo(map);

```

```js

// Charger les données (remplacez `statsPlot` par vos données réelles)
const data = statsPlot.batches[0]; 

// Vérification si les données sont bien accessibles
console.log("Data:", data);

// Créer un scatter plot entre artificial_ratio_2021 et population_2021
const scatterPlot = Plot.plot({
  width: 1000,
  height: 400,
  marks: [
    Plot.dot(data, {
      x: "artificial_ratio_2021",
      y: "population_2021",
      stroke: "red",
      fill: "red",
      opacity: 1,
      r: 4, // Taille des points
    }),
    Plot.axisX({ label: "Artificial Ratio 2021 (%)", tickFormat: d => d.toFixed(2) }),
    Plot.axisY({ label: "Population 2021 (thousands)", tickFormat: d => (d/1000) }),
  ]
});

```

```js
scatterPlot
```