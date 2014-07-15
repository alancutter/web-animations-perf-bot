#! /usr/bin/python

from __future__ import division
from __future__ import print_function

import argparse
import re
import urllib2
import sys
import xml.etree.ElementTree as ElementTree

from build import Build

from constants import (
  build_url,
  date_re,
  datetime_format,
  datetime_re,
  hosted_android_file_re,
  index_url,
  xmlns,
)


def tag(tagname):
  return '{%s}%s' % (xmlns, tagname)

def list_builds():
  builds = []
  done = False
  next_marker = ''
  print('Downloading Android build list', end='')
  while not done:
    print('.', end='')
    sys.stdout.flush()
    xml_data = urllib2.urlopen(index_url + next_marker)
    tree = ElementTree.parse(xml_data)
    done = tree.find(tag('IsTruncated')).text != 'true'
    if not done:
      next_marker = '&marker=' + tree.find(tag('NextMarker')).text
    for contents in tree.findall(tag('Contents')):
      key = contents.find(tag('Key'))
      key_match = re.match(hosted_build_key_re, key.text)
      if not key_match:
        continue
      commit = key_match.group(1)

      timestamp = contents.find(tag('LastModified'))
      datetime_match = re.match(datetime_re, timestamp.text)
      datetime = datetime_match.group(0)

      builds.append(Build(datetime, commit))
  print('done', end='\n')
  return sorted(builds, cmp=lambda bx,by: 1 if bx.datetime > by.datetime else -1)

def list_daily_builds():
  daily_builds = []
  current_date = None
  for build in list_builds():
    date = re.match(date_re, build.datetime).group(0)
    if date != current_date:
      daily_builds.append(build)
      current_date = date
  return daily_builds

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--daily', action='store_true', help='Show only the first build in each day')
  args = parser.parse_args()
  builds = list_daily_builds() if args.daily else list_builds()
  for build in builds:
    print(build)

if __name__ == '__main__':
  main()