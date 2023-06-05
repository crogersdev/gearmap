// react
import React, { useState, useEffect, useRef } from 'react';

// local imports
import GearMap from './GearMap';

// openlayers
import VectorLayer from 'ol/layer/Vector'
import VectorSource from 'ol/source/Vector'
import { transform } from 'ol/proj'
import { toStringXY } from 'ol/coordinate';

import './MapWrapper.css';

function MapWrapper(props) {

  // set intial state
  const [ map, setMap ] = useState()
  const [ featuresLayer, setFeaturesLayer ] = useState()
  const [ selectedCoord , setSelectedCoord ] = useState()

  // pull refs
  const mapElement = useRef()
  
  // create state ref that can be accessed in OpenLayers onclick callback function
  // without it, the state of this map via the `map` var (defined by useState() on line 20)
  // would remain as a reference to the state when it was created, not when it was updated
  //  https://stackoverflow.com/a/60643673
  const mapRef = useRef()
  mapRef.current = map

  // initialize map on first render - logic formerly put into componentDidMount
  useEffect( () => {

    // create and add vector source layer
    const initialFeaturesLayer = new VectorLayer({
      source: new VectorSource()
    })

    const initialMap = GearMap(mapElement.current, initialFeaturesLayer);

    // set map onclick handler
    initialMap.on('click', handleMapClick);
    initialMap.on('moveend', () => {
      console.log("a view changed");
    })

    // save map and vector layer references to state
    setMap(initialMap)
    setFeaturesLayer(initialFeaturesLayer)

  }, [])

  // update map if features prop changes - logic formerly put into componentDidUpdate
  useEffect( () => {

    if (props.features.length) { // may be null on first render

      // set features to map
      featuresLayer.setSource(
        new VectorSource({
          features: props.features // make sure features is an array
        })
      )

      // fit map to feature extent (with 100px of padding)
      map.getView().fit(featuresLayer.getSource().getExtent(), {
        padding: [100,100,100,100]
      })

    }

  }, [props.features, featuresLayer, map])

  // map click handler
  const handleMapClick = (event) => {
    console.log('foo');
    // get clicked coordinate using mapRef to access current React state inside OpenLayers callback
    //  https://stackoverflow.com/a/60643670
    const clickedCoord = mapRef.current.getCoordinateFromPixel(event.pixel);

    // transform coord to EPSG 4326 standard Lat Long
    const transormedCoord = transform(clickedCoord, 'EPSG:3857', 'EPSG:4326')

    // set React state
    setSelectedCoord(transormedCoord)
    
  }

  // render component
  return (      
    <div>
      
      <div ref={mapElement} className="map-container"></div>
      
      <div className="clicked-coord-label">
        <p>{ (selectedCoord) ? toStringXY(selectedCoord, 5) : '' }</p>
      </div>

    </div>
  ) 

}

export default MapWrapper