
import React, { useRef, useState, useEffect, useContext } from 'react';
import './App.css';
import MapContext from './components/MapContext';
import * as open_layers from 'ol';
import OLTileLayer from "ol/layer/Tile";
import { fromLonLat, get } from 'ol/proj';
import * as ol_source from "ol/source";

const osm = () => (new ol_source.OSM());

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
            </Map>
        </div>
    )
}

export default App;
