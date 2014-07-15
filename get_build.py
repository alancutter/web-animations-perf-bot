#! /usr/bin/python

from __future__ import print_function

import os

from build import Build

from constants import (
  build_url,
  extraction_directory,
)


def ensure_extraction_directory():
  if not os.path.isdir(extraction_directory):
    os.mkdir(extraction_directory)

def ensure_build_file(build):
  ensure_extraction_directory()
  build_file = build_file_template % (build.datetime, build.commit)

def get_downloaded_builds():
  downloaded_builds = set()
  for item in os.listdir('zips'):
    match = re.match(r'android-r(\d+)-(\d+-\d+-\d+)\.zip', item)
    if match:
      downloaded_builds.add((match.group(1), match.group(2)))
  return downloaded_builds

def download_build(commit):
  url = hosted_build_url_template % commit
  filename = 'zips/android-r%s-%s.zip' % build
  print('Downloading %s...' % url, end='')
  sys.stdout.flush()
  try:
    with open(filename, 'w') as destination:
      source = urllib2.urlopen(url)
      destination.write(source.read())
  except:
    os.remove(filename)
    raise
  print('saved as %s' % filename)

