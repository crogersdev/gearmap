polygons = {
        'most_of_the_usa': '''POLYGON((-123.03560917169045 45.67602408465302,-65.55514042169045 45.67602408465302,-65.55514042169045 32.510415776770685,-123.03560917169045 32.510415776770685,-123.03560917169045 45.67602408465302))'''
}

usu_school_id = 109
ball_state_school_id = 3
mwc_conf_id = 7
mac_conf_id = 6

fake_observations = [
  {
    "school_id": usu_school_id,
    "gear_type": "t-shirt",
    "wearer_gender": "male",
    "wearer_age": 30,
    "wearer_ethnicity": "asian",
    "observed_lat": 38.160476,
    "observed_long": -87.109496,
    "observation_geom": None
  },
  {
    "school_id": ball_state_school_id,
    "gear_type": "t-shirt",
    "wearer_gender": "female",
    "wearer_age": 55,
    "wearer_ethnicity": "black",
    "observed_lat": 41.191056,
    "observed_long": -74.146373,
    "observation_geom": None
  },
  {
    "school_id": usu_school_id,
    "gear_type": "t-shirt",
    "wearer_gender": "male",
    "wearer_age": 30,
    "wearer_ethnicity": "asian",
    "observed_lat": 45.8566,
    "observed_long": 2.3522, # paris.  outside of usa
    "observation_geom": None
  }
]
