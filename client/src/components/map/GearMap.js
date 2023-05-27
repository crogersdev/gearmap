import Map from 'ol/Map'
import View from 'ol/View'
import TileLayer from 'ol/layer/Tile'
import XYZ from 'ol/source/XYZ'
import { Zoom } from 'ol/control';

// create map
const GearMap = (mapElement, initialFeaturesLayer) => {
    console.log("this is the passed in mapElement: ", mapElement);
    console.log("here is the init features:", initialFeaturesLayer);
    return new Map({
        target: mapElement,
        layers: [
        
        /*
        // USGS Topo
        new TileLayer({
            source: new XYZ({
            url: 'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}',
            })
        }),

        /*
        google tile layer types

        h = roads only
        m = standard roadmap
        p = terrain
        r = somehow altered roadmap
        s = satellite only
        t = terrain only
        y = hybrid

        */

        // Google Maps Terrain
        new TileLayer({
            source: new XYZ({
            url: 'http://mt.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}',
            })
        }),

        initialFeaturesLayer
        
        ],
        view: new View({
            projection: 'EPSG:3857',
            center: [-1, 0],
            zoom: 1
        }),
        controls: [
            new Zoom(),
        ]
    })
}

export default GearMap;