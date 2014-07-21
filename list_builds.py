#! /usr/bin/python

# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import division
from __future__ import print_function

import argparse
import re
import urllib2
import sys
import xml.etree.ElementTree as ElementTree

from build import Build
from common_args import parse_argsets, step_arg

from constants import (
  build_url,
  date_re,
  datetime_format,
  datetime_re,
  hosted_build_key_re,
  index_url,
  xmlns,
)


def tag(tagname):
  return '{%s}%s' % (xmlns, tagname)

def list_every_build():
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
  for build in list_every_build():
    date = re.match(date_re, build.datetime).group(0)
    if date != current_date:
      daily_builds.append(build)
      current_date = date
  return daily_builds

def list_weekly_builds():
  weekly_builds = []
  current_week = None
  for build in list_every_build():
    date = re.match(date_re, build.datetime).group(0)
    week = date[:8] + str(int(date[-2:]) // 7)
    if week != current_week:
      weekly_builds.append(build)
      current_week = week
  return weekly_builds

def list_builds(step):
  if step == 'every':
    return list_every_build()
  if step == 'daily':
    return list_daily_builds()
  if step == 'weekly':
    return list_weekly_builds()
  assert False, 'invalid step value'

def main():
  args = parse_argsets([step_arg])
  for build in list_builds(args.step):
    print(build)

if __name__ == '__main__':
  main()
