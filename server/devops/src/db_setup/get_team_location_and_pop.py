#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
responsible for reading the cfb_teams.csv file and filling in missing
info for lat, long, and population

operates on cfb_teams.csv
1. opens to read it
2. gets a school's name and human readable school_location
3. geocodes that location for lat/longitude
4. hits census data for area get_population
5. puts all that info back into cfb_teams.csv

relies on google maps geocoder, like so:
    http://maps.google.com/maps/api/geocode/json?address=utah%20state%20university&sensor=true

"""
import requests

from os import environ
from sys import exit

from metro_areas_pop_data import state_abbreviations, metro_areas_pop
from town_pop_data import town_pops


def get_latlong(row_data):
    lat = row_data.get('latitude', None)
    lon = row_data.get('longitude', None)

    if lat is not None and lon is not None:
        print("already had lat and long for %s: lat %s, long %s" %
              (row_data['school'], row_data['latitude'], row_data['longitude']))
        return

    print("getting lat / long for %s" % row_data['school'],)

    url = geocode_url + row_data['school'] + '&key=' + google_geocode_api_key
    resp = requests.get(url)

    if resp.status_code != 200:
        print("problem getting lat/long: %s" % resp.text)
        print("this was my url: %s" % url)
        exit()

    try:
        print("lat: %s, long: %s" % (
            resp.json()['results'][0]['geometry']['location']['lat'],
            resp.json()['results'][0]['geometry']['location']['lng']))
    except Exception as e:
        print("problem accessing response value for lat/long geocode")
        print("url: %s" % url)
        print("respose:")
        print(resp.json())
        exit()

    row_data['latitude'] = str(
        resp.json()['results'][0]['geometry']['location']['lat'])
    row_data['longitude'] = str(
        resp.json()['results'][0]['geometry']['location']['lng'])


def get_population(row_data):
    population = row_data.get('population', None)
    if population:
        print("had population for %s, %s: %s" % (
            row_data['city'], row_data['state'], row_data['population']))
        return

    # first check metro areas
    for (key, value) in metro_areas_pop.iteritems():
        if row_data.get("city", None) in key:
            print("found population for METRO AREA %s: %s" % (
                  row_data["city"], metro_areas_pop[key]))
            row_data["population"] = value
            return

    # now check for towns
    for (key, value) in town_pops.iteritems():
        if row_data.get("city", None) in key:
            print("found population for TOWN %s: %s" % (row_data["city"], value))
            row_data["population"] = value
            return

    # town not found in the town pops, so let's see if it's within 10
    # miles (or 17000 meters away from a metro area
    if row_data.get("population", None) is '':
        for metro_list_entry in [mk.split(', ') for mk in metro_areas_pop.keys()]:
            metro_area = metro_list_entry[0]
            metro_states = metro_list_entry[1]
            state_abbrev = state_abbreviations[row_data.get('state', 'VA')]
            if state_abbrev not in metro_list_entry[1]:
                continue

            origins = "&origins=%s%%2c%s" % (
                row_data['city'].replace(' ', '+'), row_data['state'])
            destinations = "&destinations=%s%%2c%s" % (
                metro_area.replace(' ', '+'), metro_states)
            url = distance_url + origins + destinations + "&key=" + google_distance_matrix_api_key
            resp = requests.get(url)

            if resp.status_code == 200:
                try:
                    dist_meters = resp.json()['rows'][0]['elements'][0]['distance']['value']

                    if dist_meters < 17000:
                        for city in metro_area.split('-'):
                            for (key, value) in metro_areas_pop.iteritems():
                                if city in key:
                                    print("town %s was within 10 miles of %s, \
                                          population: %s" % (row_data["city"],
                                                             city, value))
                                    row_data['population'] = value
                                    return
                except Exception as e:
                    print("problem processing response:\n", resp.json())
                    print("error was: %s", e)
                    exit()


if __name__ == '__main__':

    try:
        census_api_key = environ['CENSUS_API_KEY']
        google_geocode_api_key = environ['GOOGLE_GEOCODE_API_KEY']
        google_distance_matrix_api_key = environ['GOOGLE_DISTANCE_MATRIX_API_KEY']
    except KeyError as e:
        print("Either Census or Google Geocode API key not present.")
        print("Please export CENSUS_API_KEY=your_key_here and/or")
        print("       export GOOGLE_GEOCODE_API_KEY=your_key_here")
        print("       export GOOGLE_DISTANCE_MATRIX_API_KEY=your_key_here")
        exit(0)

    dataout = open('cfb_teams_final.csv', 'w')

    geocode_url = "https://maps.google.com/maps/api/geocode/json?address=%20university%20of%20"
    distance_url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial"

    with open('cfb_teams.csv', 'r') as src_file:
        for count, line in enumerate(src_file):
            line = line.rstrip('\r\b')
            line = line.rstrip('\r\n')
            if line == '':
                continue
            line = line.split(',')

            if count == 0:
                header = line
                print("header was: ", header)
                dataout.write(','.join(line) + '\r\n')
                continue

            row_data = dict(zip(header, line))

            # get_latlong
            get_latlong(row_data)
            # get population if possible
            get_population(row_data)

            row_to_write = ''
            for h in header:
                row_to_write += str(row_data[h]) + ','

        row_to_write = row_to_write[:-1] + '\n'
        dataout.write(row_to_write)

    dataout.close()
