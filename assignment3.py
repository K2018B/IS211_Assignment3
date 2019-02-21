#!/usr/bin/python
# -*- coding: utf-8 -*-
"""IS 211 Assignment Week 3"""
from __future__ import division
from urllib2 import Request, urlopen, URLError, HTTPError
import csv
import re
import argparse
import sys
import logging
from datetime import datetime

TESTINGURL = 'http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv'

def main():
    """specifying TESTINGURL"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='URL to lookup', default=TESTINGURL)
    args = parser.parse_args()
    if args:
        csvdata = downloadData(args.url)
    else:
        LOGGER.error("No URL entered! Specify --url is mandatory")
        sys.exit()
    weblog = processData(csvdata)
    imageSearch(weblog)
    browserSearch(weblog)
    timeSearch(weblog)

def downloadData(url):
    """download the CSV from TESTINGURL or URL specified"""
    try:
        req = Request(url)
        response = urlopen(req)
    except HTTPError as error:
        LOGGER.error(error)
        sys.exit()
    except URLError:
        LOGGER.error('Unable to retrieve CSV file')
        sys.exit()
    return response

def processData(csvdata):
    """imports .csv file from TESTINGURL"""
    fieldnames = ("filepath", "datetime", "browser", "status", "request_size")
    datafile = csv.DictReader(csvdata, fieldnames=fieldnames)
    dictList = []
    for line in datafile:
        dictList.append(line)
    return dictList

def imageSearch(datafile):
    """searches values for extensions ending in jpg, png and gif..."""
    images = 0
    for row in datafile:
        for key, value in row.items():
            if key == 'filepath':
                if re.search('.(jpg|png|gif|jpeg)', value, re.IGNORECASE):
                    images += 1
    print("Image requests account for {}% of all requests").format(images/len(datafile)*100)

def browserSearch(datafile):
    """searches datafile for browsers"""
    browsers = {'Firefox': 0, 'Chrome': 0, 'Internet Explorer': 0, 'Safari': 0}
    for row in datafile:
        for key, value in row.items():
            if key == 'browser':
                if re.search('firefox', value, re.IGNORECASE):
                    browsers['Firefox'] += 1
                if re.search('chrome', value, re.IGNORECASE):
                    browsers['Chrome'] += 1
                if re.search('ie', value, re.IGNORECASE):
                    browsers['Internet Explorer'] += 1
                if re.search('safari', value, re.IGNORECASE):
                    browsers['Safari'] += 1
    print("popular browser of the day is {}.").format(max(browsers, key=browsers.get))

def timeSearch(datafile):
    """build directory for each hour..."""
    activehours = {}
    for row in datafile:
        for key, value in row.items():
            if key == 'datetime':
                dFormat = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                if dFormat.hour in activehours:
                    activehours[dFormat.hour] += 1
                else:
                    activehours[dFormat.hour] = 1
    for hour in xrange(0, 24):
        print("Hour {} has {} hits").format(hour, activehours.get(hour, 0))

if __name__ == '__main__':
    LOGGER = logging.getLogger('assignment3')
    LOGGER.setLevel(logging.ERROR)
    try:
        LOGFILE = logging.FileHandler('errors.log')
    except IOError:
        print "Unable to open log file"
    LOGFILE.setLevel(logging.DEBUG)
    FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    LOGFILE.setFormatter(FORMATTER)
    LOGGER.addHandler(LOGFILE)
    main()
