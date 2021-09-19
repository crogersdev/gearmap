
import React, { useRef, useState, useEffect, useContext } from 'react';
import MapContext from './components/MapContext';

import * as open_layers from 'ol';
import * as ol_source from "ol/source";

import OLTileLayer from "ol/layer/Tile";
import OLVectorLayer from "ol/layer/Vector";
import GeoJSON from "ol/format/GeoJSON";

import { fromLonLat, get } from 'ol/proj';
import { Circle as CircleStyle, Fill, Stroke, Style } from "ol/style";
import { Vector as VectorSource } from 'ol/source';

import './App.css';

function vector({ features }) {
	return new VectorSource({
		features
	});
}

const osm = () => (new ol_source.OSM());

const featureStyles =   {
    Point: new Style({
    image: new CircleStyle({
      radius: 10,
      fill: null,
      stroke: new Stroke({
        color: "magenta",
      }),
    }),
  }),
  Polygon: new Style({
    stroke: new Stroke({
      color: "blue",
      lineDash: [4],
      width: 3,
    }),
    fill: new Fill({
      color: "rgba(0, 0, 255, 0.1)",
    }),
  }),
  MultiPolygon: new Style({
    stroke: new Stroke({
      color: "blue",
      width: 1,
    }),
    fill: new Fill({
      color: "rgba(0, 0, 255, 0.1)",
    }),
  }),
}

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

const TileLayer = ({ source, zIndex = 0 }) => {
    const { map } = useContext(MapContext);
    useEffect(() => {
        if (!map) return;

        let tileLayer = new OLTileLayer({
            source,
            zIndex
        });
        map.addLayer(tileLayer);
        tileLayer.setZIndex(zIndex);

    
        return () => {
            if (map) {
                map.removeLayer(tileLayer);
            }
        };
    }, [map]);

    return null;
};

const VectorLayer = ({source, style, zIndex = 0}) => {
    const { map } = useContext(MapContext);

    useEffect(() => {
        if (!map) return;

        let vectorLayer = new OLVectorLayer({
            source,
            style
        });

        map.addLayer(vectorLayer);
        vectorLayer.setZIndex(zIndex);

        return () => {
            if (map) map.removeLayer(vectorLayer);
        };
    }, [map]);

    return null;

};

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
