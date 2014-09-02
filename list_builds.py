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
from datetime import datetime as Datetime
import os
import re
import urllib2
import subprocess
import sys
import time
import xml.etree.ElementTree as ElementTree

from build import Build
from common_args import chromium_src_arg, parse_argsets, step_arg

from constants import (
  build_url,
  commit_datetimes_path,
  date_re,
  datetime_format,
  datetime_re,
  commit_position_tag,
  hosted_build_key_re,
  index_url,
  list_cache_directory,
  xmlns,
)


def fetch_chromium_logs(chromium_src):
  print('Refreshing Chromium git log.')
  subprocess.check_call(['git', 'fetch', 'origin'], cwd=chromium_src)

def load_cached_commit_datetimes():
  commit_datetimes = {}
  if not os.path.exists(commit_datetimes_path):
    return commit_datetimes
  with open(commit_datetimes_path) as f:
    for line in f:
      commit, datetime = line.strip().split()
      commit_datetimes[commit] = datetime
  return commit_datetimes

def tag(tagname):
  return '{%s}%s' % (xmlns, tagname)

def datetime_for_commit(cached_commit_datetimes, chromium_src, commit):
  # Attempt to fetch from cache.
  if commit in cached_commit_datetimes:
    return cached_commit_datetimes[commit]

  # Read from git logs.
  command = ['git', 'log', '-1', '--format=%ct']
  if len(commit) < 10 and commit.isdigit(): # commit position
    commit_position = int(commit)
    git_commit = subprocess.check_output(['git', 'log', '-1', '--format=%H', '--grep=' + (commit_position_tag % commit_position), 'origin/master'], cwd=chromium_src).strip()
    assert git_commit, 'Commit must exist at position %s' % commit_position
    command.append(git_commit)
  else: # git revision
    assert commit
    command.append(commit)
  timestamp = int(subprocess.check_output(command, cwd=chromium_src))
  datetime = Datetime.utcfromtimestamp(timestamp).strftime(datetime_format)

  # Store in cache.
  print('Caching commit %s datetime %s.' % (commit, datetime))
  cached_commit_datetimes[commit] = datetime
  if not os.path.exists(list_cache_directory):
    os.mkdir(list_cache_directory)
  with open(commit_datetimes_path, 'a') as f:
    f.write('%s %s\n' % (commit, datetime))

  return datetime

def list_every_build(chromium_src):
  fetch_chromium_logs(chromium_src)
  cached_commit_datetimes = load_cached_commit_datetimes()
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
      datetime = datetime_for_commit(cached_commit_datetimes, chromium_src, commit)
      builds.append(Build(datetime, commit))
  print('done', end='\n')
  return sorted(builds, cmp=lambda bx,by: 1 if bx.datetime > by.datetime else -1)

def list_daily_builds(chromium_src):
  daily_builds = []
  current_date = None
  for build in list_every_build(chromium_src):
    date = re.match(date_re, build.datetime).group(0)
    if date != current_date:
      daily_builds.append(build)
      current_date = date
  return daily_builds

def list_weekly_builds(chromium_src):
  weekly_builds = []
  current_week = None
  for build in list_every_build(chromium_src):
    date = re.match(date_re, build.datetime).group(0)
    week = date[:8] + str(int(date[-2:]) // 7)
    if week != current_week:
      weekly_builds.append(build)
      current_week = week
  return weekly_builds

def list_builds(chromium_src, step='every', from_datetime=''):
  if step == 'every':
    builds = list_every_build(chromium_src)
  elif step == 'daily':
    builds = list_daily_builds(chromium_src)
  elif step == 'weekly':
    builds = list_weekly_builds(chromium_src)
  else:
    assert False, 'invalid step value'
  return [build for build in builds if build.datetime >= from_datetime]

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--from-datetime', type=str, default='', help='The earliest datetime for listing Android builds. Defaults to the beginning of time. Use "latest" to list only the latest build.')
  args = parse_argsets([chromium_src_arg, step_arg], parser)
  if args.from_datetime == 'latest':
    print(list_builds(args.chromium_src, args.step)[-1])
    return
  for build in list_builds(args.chromium_src, args.step, args.from_datetime):
    print(build)

if __name__ == '__main__':
  main()
