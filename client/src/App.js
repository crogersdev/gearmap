
import React, { useRef, useState, useEffect } from 'react';
import MapContext from './components/MapContext';

import * as open_layers from 'ol';
import * as ol_source from "ol/source";

import GeoJSON from "ol/format/GeoJSON";

import TileLayer from './components/layers/TileLayer';
import VectorLayer from './components/layers/VectorLayer';

import { fromLonLat, get } from 'ol/proj';
import { Vector as VectorSource } from 'ol/source';

import featureStyles from './components/features';

import './App.css';

function vector({ features }) {
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

const Map = ({ children, zoom, center }) => {
    const mapRef = useRef();

    const [map, setMap] = useState(null);

    //on component mount
    useEffect(() => {
        let options = {
            view: new open_layers.View({ zoom, center }),
            layers: [],
            controls: [],
            overlays: []
        };

        let mapObject = new open_layers.Map(options);
        mapObject.setTarget(mapRef.current);
        setMap(mapObject);

        return () => mapObject.setTarget(undefined);
    }, []);

    useEffect((map) => {
        if (!map) return;

        map.getView().setZoom(zoom);
    }, [zoom])

    useEffect((map) => {
        if (!map) return;

        map.getview().setCenter(center);
    }, [center])

    return (
        <MapContext.Provider value={{ map }}>
            <div ref={mapRef} className="ol-map">
                { children }
            </div>
        </MapContext.Provider>
    )
}

const App = () => {

    const [center, setCenter] = useState([-94.9065, 38.9884]);
    const [zoom, setZoom] = useState(9);

    return (
        <div>
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
