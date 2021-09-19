import mapboxgl from 'mapbox-gl';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import debounce from 'lodash/debounce';

import 'mapbox-gl/dist/mapbox-gl.css';

import images from '../assets';


const mapStateToProps = (state) => ({
    mapInfo: state.mapUpdateReducer.mapInfo,
    observationData: state.mapUpdateReducer.observationData,
});

class Mapbox extends Component {
    constructor(props) {
        super(props);

        this.debounceUpdateMapInfo = debounce(
            this.debounceUpdateMapInfo,
            300 // ms to delay
        );
    }

    debounceUpdateMapInfo = (mapInfo) => {
        this.props.updateMapInfo(mapInfo);
    };

    handleMapChange = (mapInfo) => {
        this.debounceUpdateMapInfo(mapInfo);
    };

    loadSchoolIcons = (mapbox_map) => {
        Object.keys(images).forEach((image_name) => {
            mapbox_map.loadImage(
                images[image_name], (error, image) => {
                    if (error) throw error;
                    mapbox_map.addImage(image_name.slice(0, -4), image);
                }
            )
        });
    };

    componentDidMount = () => {
        this.map = new mapboxgl.Map({
            container: this.mapContainer,
            style: 'mapbox://styles/mapbox/dark-v10',
            center: [-117.5, 47.5],
            zoom: 8,
        })

        let map = this.map;

        // TRICKY: The context of 'this' changes inside the mapboxgl
        //         on move method.  Soooo we get around that by wrapping
        //         the move handler.
        let mapChangeTrigger = this.handleMapChange;

        let lng = 0, lat = 0, zoom = 0;
        let boundingBox = {};

        map.addControl(new mapboxgl.NavigationControl());

        // (indirectly) set component state on map move
        map.on('move', () => {
            lat = map.getCenter().lat.toFixed(4);
            lng = map.getCenter().lng.toFixed(4);
            zoom = map.getZoom().toFixed(2);
            boundingBox = {
                north: map.getBounds().getNorth(),
                east: map.getBounds().getEast(),
                south: map.getBounds().getSouth(),
                west: map.getBounds().getWest(),
            };
            let bb = boundingBox;
            let boundingBoxPolygon = "POLYGON(( " + bb.east + " " + bb.north + ", " + bb.west + " " + bb.north + ", " + bb.west + " " + bb.south + ", " + bb.east + " " + bb.south + ", " + bb.east + " " + bb.north + " ))";

            mapChangeTrigger({
                lat,
                lng,
                zoom,
                boundingBox,
                boundingBoxPolygon,
            });
        });

        map.on('load', () => {
            this.loadSchoolIcons(map);
            
            map.addSource("observations_geojson", {
                type: "geojson",
                data: this.props.observationData.observations.geo_json,
                cluster: true,
                clusterMaxZoom: 14, // Max zoom to cluster points on
                clusterRadius: 50 // Radius of each cluster when clustering points (defaults to 50)
            });
            map.addLayer({
                id: "clusters",
                type: "circle",
                source: "observations_geojson",
                filter: ["has", "point_count"],
                paint: {
                    // Use step expressions (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-step)
                    // with three steps to implement three types of circles:
                    //   * Blue, 20px circles when point count is less than 100
                    //   * Yellow, 30px circles when point count is between 100 and 750
                    //   * Pink, 40px circles when point count is greater than or equal to 750
                    "circle-color": [
                        "step",
                        ["get", "point_count"],
                        "#cccccc",
                        100,
                        "#999999",
                        750,
                        "#666666"
                    ],
                    "circle-radius": [
                        "step",
                        ["get", "point_count"],
                        20,
                        100,
                        30,
                        750,
                        40
                    ]
                }
            });
            map.addLayer({
                id: "cluster-count",
                type: "symbol",
                source: "observations_geojson",
                filter: ["has", "point_count"],
                layout: {
                    "text-field": "{point_count_abbreviated}",
                    "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
                    "text-size": 12
                }
                });
            map.addLayer({
                id: 'observations_layer',
                type: 'symbol',
                source: 'observations_geojson',
                filter: ["!", ["has", "point_count"]],
                layout: {
                    'icon-allow-overlap': true,
                    "icon-image": '{icon}',
                    "text-field": "{title}",
                    "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
                    "text-offset": [0, 0.6],
                    "text-anchor": "top"
                },
                paint: {
                    'text-color': '#ffffff',
                }
            });

            lat = map.getCenter().lat.toFixed(4);
            lng = map.getCenter().lng.toFixed(4);
            zoom = map.getZoom().toFixed(2);
            boundingBox = {
                north: map.getBounds().getNorth(),
                east: map.getBounds().getEast(),
                south: map.getBounds().getSouth(),
                west: map.getBounds().getWest(),
            };
            let bb = boundingBox;
            let boundingBoxPolygon = "POLYGON(( " + bb.east + " " + bb.north + ", " + bb.west + " " + bb.north + ", " + bb.west + " " + bb.south + ", " + bb.east + " " + bb.south + ", " + bb.east + " " + bb.north + " ))";

            mapChangeTrigger({
                lat,
                lng,
                zoom,
                boundingBox,
                boundingBoxPolygon,
            });
        });
    }

    shouldComponentUpdate = (nextProps, nextState) => {
        return (this.props === nextProps ? false : true);
    }

    componentDidUpdate = () => {
        let observations_data = this.props.observationData.observations.data;
        this.map.getSource('observations_geojson').setData(observations_data);
    }

    componentWillUnmount = () => {
        this.map.remove();
    }

    render = () => {
        const map_canvas_style = {
            position: 'absolute',
            bottom: 0,
            width: '100%',
            height: '100%',
        };

        // TRICKY: I had wanted to use a dedicated css file for this component but
        // when converting the above map_canvas_style to a css file
        // and then including it and using it with the className prop
        // nothing rendered...  soooooooo gonna just go with what i got here.
        return (
            <div 
                style={map_canvas_style}
                ref={el => this.mapContainer = el} 
            />
        );
    }
}

export default connect(
    mapStateToProps
)(Mapbox);

Mapbox.propTypes = {
    updateMapInfo: PropTypes.func.isRequired,
}
