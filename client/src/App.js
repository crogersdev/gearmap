
import React, { useState } from 'react';

import * as ol_source from "ol/source";

import GeoJSON from "ol/format/GeoJSON";

import TileLayer from './components/layers/TileLayer';
import VectorLayer from './components/layers/VectorLayer';
import Map from './components/map/Map.js';

import { fromLonLat, get } from 'ol/proj';
import { Vector as VectorSource } from 'ol/source';

import featureStyles from './components/features';

import './App.css';

const vector = ({ features }) => {
	return new VectorSource({
		features
	});
}

const osm = () => (new ol_source.OSM());

const geoJsonObject = {
    "type": "FeatureCollection",
    "features": [
    {
        "type": "Feature",
        "properties": {
            "kind": "county",
            "name": "Wyandotte",
            "state": "KS"
        },
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [
            [
                [
                [-94.8627, 39.202],
                [-94.901, 39.202],
                [-94.9065, 38.9884],
                [-94.8682, 39.0596],
                [-94.6053, 39.0432],
                [-94.6053, 39.1144],
                [-94.5998, 39.1582],
                [-94.7422, 39.1691],
                [-94.7751, 39.202],
                [-94.8627, 39.202]
                ]
            ]
            ]
        }
        }
    ]
}

const App = () => {

    const [center, setCenter] = useState([-94.9065, 38.9884]);
    const [zoom, setZoom] = useState(9);

    return (
        <div style={{ height: '100vh', backgroundColor: 'red' }}>
            <Map center={fromLonLat(center)} zoom={zoom}>
                <TileLayer source={osm()} zIndex={0} />
                <VectorLayer
                    source={vector({
                        features: new GeoJSON().readFeatures(geoJsonObject,
                            {featureProjection: get("EPSG:3857"),
                        }),
                    })} 
                    style={featureStyles.MultiPolygon}
                />
            </Map>
        </div>
    )
}

export default App;
