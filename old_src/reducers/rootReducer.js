export const UPDATE_MAP_INFO = "UPDATE_MAP_INFO";
export const FETCH_OBSERVATIONS_BEGIN = "FETCH_OBSERVATIONS_BEGIN";
export const FETCH_OBSERVATIONS_SUCCESS = "FETCH_OBSERVATIONS_SUCCESS";
export const FETCH_OBSERVATIONS_ERROR = "FETCH_OBSERVATIONS_ERROR";
export const APPLY_FILTERS_BEGIN = "APPLY_FILTERS_BEGIN";
export const APPLY_FILTERS_SUCCESS = "APPLY_FILTERS_SUCCESS";

const initialState = {
    searchValue: 'Search...',
    mapInfo: "no mapInfo yet",
    observationData: {
        observations: {
            num_observations: 0,
            geo_json: {
                "type": "FeatureCollection",
                "features": []
              }
        }
    },
}

export const mapUpdateReducer = (state = initialState, action) => {
    switch (action.type) {
        case APPLY_FILTERS_BEGIN:
            state = {
                ...state,
            }
            break;
        case APPLY_FILTERS_SUCCESS:
            state = {
                ...state,
            }
            break;
        case FETCH_OBSERVATIONS_BEGIN:
            state = {
                ...state,
            }
            break;
        case FETCH_OBSERVATIONS_ERROR:
            state = {
                ...state,
            }
            break;
        case FETCH_OBSERVATIONS_SUCCESS:
            state = {
                ...state,
                observationData: {
                    observations: action.payload.data
                }
            }
            break;
        case UPDATE_MAP_INFO:
            state = {
                ...state,
                mapInfo: action.payload
            };
            break;
        default:
            break;
    }

    return state;
};
