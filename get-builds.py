#! /usr/bin/python

from __future__ import division
from __future__ import print_function

from datetime import datetime
import os
import re
import urllib2
import sys
import xml.etree.ElementTree as ElementTree

builds_url = 'http://commondatastorage.googleapis.com/chromium-browser-continuous/?prefix=Android/'
date_format = '%Y-%m-%d'
xmlns = 'http://doc.s3.amazonaws.com/2006-03-01'

last_print_length = 0

def start_reprint(text, end=''):
  global last_print_length
  last_print_length = 0
  print(text, end=end)

def reprint(text, end=''):
  global last_print_length
  print('\b' * last_print_length, end=end)
  print(text, end=end)
  last_print_length = len(text)

def tag(tagname):
  return '{%s}%s' % (xmlns, tagname)

def percentage(current, total):
  return '%s%% ' % int(round(100 * current / total))

def get_downloaded_builds():
  downloaded_builds = set()
  for item in os.listdir('.'):
    match = re.match(r'android-r(\d+)-(\d+-\d+-\d+)\.zip', item)
    if match:
      downloaded_builds.add((match.group(1), match.group(2)))
  return downloaded_builds

def get_current_builds():
  current_builds = set()
  done = False
  next_marker = ''
  first_timestamp = None
  last_seen_timestamp = None
  start_reprint('Downloading Android build list...')
  while not done:
    if first_timestamp:
      reprint(percentage(
        (last_seen_timestamp - first_timestamp).total_seconds(),
        (datetime.utcnow() - first_timestamp).total_seconds()))
    else:
      reprint('0%')
    sys.stdout.flush()
    xml_data = urllib2.urlopen(builds_url + next_marker)
    tree = ElementTree.parse(xml_data)
    done = tree.find(tag('IsTruncated')).text != 'true'
    if not done:
      next_marker = '&marker=' + tree.find(tag('NextMarker')).text
    for contents in tree.findall(tag('Contents')):
      key = contents.find(tag('Key'))
      key_match = re.match(r'Android/(\d+)/chrome-android\.zip', key.text)
      if not key_match:
        continue
      revision = key_match.group(1)

      timestamp = contents.find(tag('LastModified'))
      date_match = re.match(r'^[\d-]{10}', timestamp.text)
      date = date_match.group(0)

      current_builds.add((revision, date))

      if not first_timestamp:
        first_timestamp = datetime.strptime(date, date_format)
      last_seen_timestamp = datetime.strptime(date, date_format)
  reprint('complete', end='\n')
  print(current_builds)
  return current_builds

def download_build(build):
  url = '%sAndroid/%s/chrome-android.zip' % (builds_url, build[0])
  filename = 'android-r%s-%s.zip' % build
  print('Downloading %s...' % url, end='')
  sys.stdout.flush()
  with open(filename, 'w') as destination:
    source = urllib2.urlopen(url)
    destination.write(source.read())
  print('saved as %s' % filename)

def download_builds(builds):
  print('Downloading %s builds' % len(builds))
  count = 0
  for build in sorted(builds, reverse=True):
    count += 1
    print('(%s)' % percentage(count, len(builds)), end='')
    download_build(build)

def main():
  downloaded_builds = get_downloaded_builds()
  current_builds = get_current_builds()
  missing_builds = current_builds - downloaded_builds
  download_builds(missing_builds)

if __name__ == '__main__':
  main()