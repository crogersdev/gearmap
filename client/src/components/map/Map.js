import React, { useRef, useState, useEffect } from 'react';
import * as open_layers from 'ol';
import MapContext from '../MapContext';

import './Map.css';

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
        map.getview().setCenter(center);
    }, [zoom, center])

    const map_canvas_style = {
        width: '100%',
        height: '100%',
    };

    return (
        <MapContext.Provider value={{ map }}>
            <div ref={mapRef} style={ map_canvas_style } className="ol-map">
                { children }
            </div>
        </MapContext.Provider>
    )
}

export default Map;