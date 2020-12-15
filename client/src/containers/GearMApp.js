import React, { Component } from 'react';
import { connect } from 'react-redux';

import Mapbox from '../components/Mapbox';
import { asyncUpdateMapInfo, asyncApplyFilters } from '../actions/actionTypes';
import ControlPanel from '../components/ControlPanel';


// TRICKY: using ('s and )'s to wrap the return object to force ES* (5? 6? 7?)
//         to return an object literal. Note: The {}'s around the return object
//         are NOT intended to wrap the object literal.  They are intended to
//         define the return clause for the fat arrow function.  It's a
//         shortcut around having to type something like this:
// ...stuff... => { return { somekey: some_value } }
const mapStateToProps = (state) => ({
    mapInfo: state.mapInfo,
    observationData: state.observationData,
});

const mapDispatchToProps = (dispatch) => ({
    updateMapInfo: (mapInfo) => {
        dispatch(asyncUpdateMapInfo(mapInfo));
    },
    applyFilters: (filters, mapInfo) => {
        dispatch(asyncApplyFilters(filters, mapInfo));
    }
});

class GearMApp extends Component {

    render() {

        return (
            <div>
                <ControlPanel 
                    updateMapInfo={
                        (mapInfo) => { this.props.updateMapInfo(mapInfo) }
                    }
                    applyFilters={
                        (filters) => { this.props.applyFilters(filters) }
                }/>
                <Mapbox updateMapInfo={
                    (mapInfo) => { this.props.updateMapInfo(mapInfo) }
                }/>
            </div>
        );
    }
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(GearMApp);
