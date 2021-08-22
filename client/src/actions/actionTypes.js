import axios from 'axios';

import {
    APPLY_FILTERS_BEGIN,
    APPLY_FILTERS_SUCCESS,
    FETCH_OBSERVATIONS_BEGIN,
    FETCH_OBSERVATIONS_ERROR,
    FETCH_OBSERVATIONS_SUCCESS,
    UPDATE_MAP_INFO,
} from '../reducers/rootReducer';

export const updateMapInfo = (mapInfo) => {
    return {
        type: UPDATE_MAP_INFO,
        payload: mapInfo,
    };
}

export const applyFilters = (filters) => {
    console.log('inside applyFilters');
    return {
        type: "APPLY_FILTERS",
        payload: filters,
    }
}

export const asyncUpdateMapInfo = (mapInfo) => {
    return (dispatch) => {
        dispatch({ type: FETCH_OBSERVATIONS_BEGIN, payload: "" });
        dispatch({ type: UPDATE_MAP_INFO, payload: mapInfo });

        let urlStem = "http://server:5001/observations"
        let encodedURL = encodeURI(urlStem)

        axios.post(encodedURL, {
            bbox: mapInfo.boundingBoxPolygon,
        })
        .then(
            (response) => {
                if (response.status === 200) {
                    return response.data;
                }
                console.log(response)
                throw new Error("404");
            }
        )
        .then((observationData) => dispatch(
            { type: FETCH_OBSERVATIONS_SUCCESS, payload: observationData })
        )
        .catch(
            { type: FETCH_OBSERVATIONS_ERROR, payload: "whoops."}
        );
    };
};

export const asyncApplyFilters = (state) => {
    return (dispatch) => {
        dispatch({ type: APPLY_FILTERS_BEGIN, payload: "" });
        dispatch({ type: UPDATE_MAP_INFO, payload: state.mapInfo });

        let urlStem = "http://localhost:5001/observations_by_schools"
        let encodedURL = encodeURI(urlStem)

        axios.post(encodedURL, {
            bbox: state.mapInfo.boundingBoxPolygon,
            school_names: state.searchValue
        })
        .then(
            (response) => {
                if (response.status === 200) {
                    return response.data;
                }
                console.log(response)
                throw new Error("404");
            }
        )
        .then((observationData) => dispatch(
            { type: FETCH_OBSERVATIONS_SUCCESS, payload: observationData })
        )
        .then(
            () => dispatch(
                { type: APPLY_FILTERS_SUCCESS, payload: "" })
        )
        .catch(
            { type: FETCH_OBSERVATIONS_ERROR, payload: "whoops."}
        );
    };
};
