import React from 'react';
import ReactDOM from 'react-dom';
import { createStore, combineReducers, applyMiddleware } from 'redux';
import { createLogger } from 'redux-logger';
import { Provider } from 'react-redux';
import thunk from 'redux-thunk'

import { mapUpdateReducer } from './reducers/rootReducer';
import mapboxgl from 'mapbox-gl';
import registerServiceWorker from './registerServiceWorker';
import './index.css';

import GearMApp from './containers/GearMApp';

mapboxgl.accessToken = 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4M29iazA2Z2gycXA4N2pmbDZmangifQ.-g_vE53SD2WrJ6tFX7QHmA';

const reduxLogger = createLogger({});

// TRICKY: The order here matters!  Without putting thunk first, the
//         reduxLogger misses out on the definition of the action creators
//         and the console will log 'undefined' as the action...
const middlewares = [thunk, reduxLogger]

const store = createStore(
    combineReducers({ mapUpdateReducer }),
    {},
    applyMiddleware(...middlewares)
);

ReactDOM.render(
    <Provider store={store}>
        <GearMApp />
    </Provider>, 
    document.getElementById('root')
);
registerServiceWorker();
