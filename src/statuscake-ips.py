#!/usr/bin/env python

"""
This is a simple script for retrieving a list of ips used by StatusCake.

"""

from __future__ import print_function

import argparse
import sys
import requests
import json
import simplejson

from iso3166 import countries


def main(cmdline=None):

    """
    The main function. This takes the command line arguments provided and parse them.
    """

    parser = make_parser()

    args = parser.parse_args(cmdline)

    if args.country_code:
        try:
            country = countries.get(args.country_code)
        except KeyError:
            print("Invalid country code: " + args.country_code)
            return 1

        print("Retrieving IPs for %s (%s)" % (country.name, args.country_code))
    else:
        print("Retrieving ALL IPs")

    return get_ip_list(args.country_code)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='Retrieve StatusCake IPS')

    parser.add_argument('-v', '--verbose', help='Help with debugging', action="store_true")
    parser.add_argument('-c', '--country-code', type=str, help='ISO Country code')
    return parser


def get_ip_list(country_code):

    """
    Retrieve the actual list
    """
    url = "https://app.statuscake.com/Workfloor/Locations.php?format=json"

    response = requests.get(url, allow_redirects=True)
    try:
        data = response.json()
    except simplejson.errors.JSONDecodeError:
        print("Invalid json returned by server")
        return 1

    for key, dict in data.iteritems():
        if country_code is None or dict['countryiso'] == country_code:
            print("%s; # %s - %s " % (dict['ip'], dict['countryiso'], dict['title']))


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
