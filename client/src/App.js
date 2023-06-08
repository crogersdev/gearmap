import './App.css';

// react
import React, { useState, useEffect } from 'react';

// openlayers
import GeoJSON from 'ol/format/GeoJSON'

// components
import MapWrapper from './components/map/MapWrapper'

function App() {

// set intial state
const [ features, setFeatures ] = useState([])

// initialization - retrieve GeoJSON features from Mock JSON API get features from mock 
//  GeoJson API (read from flat .json file in public directory)
useEffect( () => {
  fetch('http://server:5001/observations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(!!!MUST GET BBOX FROM MAPWRAPPER AND GEARMAP!!!)
  })
    .then(response => response.json())
    .then(fetchedFeatures => {
      console.log("this guy got called")
      console.log(fetchedFeatures)

      // parse fetched geojson into OpenLayers features
      //  use options to convert feature from EPSG:4326 to EPSG:3857
      const wktOptions = {
        dataProjection: 'EPSG:4326',
        featureProjection: 'EPSG:3857'
      }
      const parsedFeatures = new GeoJSON().readFeatures(fetchedFeatures, wktOptions)

      // set features into state (which will be passed into OpenLayers
      //  map component as props)
      setFeatures(parsedFeatures)
    })
  },[]
)

return (
  <div className="App">
    
    <div className="app-label">
      <p>React Functional Components with OpenLayers Example</p>
      <p>Click the map to reveal location coordinate via React State</p>
    </div>
    
    <MapWrapper features={features} />

  </div>
  )
}

export default App
