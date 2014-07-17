#! /usr/bin/python

from __future__ import print_function

import argparse
import os
import re
import sys
import urllib2
import zipfile

from build import Build
from common_args import parse_argsets, build_args

from constants import (
  build_url,
  datetime_format,
  datetime_re,
  hosted_build_url_template,
  archive_directory,
  archived_build_file_template,
  archived_build_file_inner_path,
  extraction_directory,
  extracted_build_file_template,
)


def download_file(url, destination):
  print('Downloading\n\t%s\nas\n\t%s\n...' % (url, destination), end='')
  sys.stdout.flush()
  try:
    with open(destination, 'w') as writer:
      source = urllib2.urlopen(url)
      writer.write(source.read())
  except:
    os.remove(destination)
    raise
  print('done')

def extract_file(source, inner_path, destination):
  print('Extracting\n\t%s\nfrom\n\t%s\nas\n\t%s\n...' % (inner_path, source, destination), end='')
  with zipfile.ZipFile(source, 'r') as archive:
    with open(destination, 'w') as writer:
      writer.write(archive.read(inner_path))
  print('done')

def ensure_directory(directory):
  if not os.path.exists(directory):
    os.mkdir(directory)

def ensure_archived_build_file(build):
  ensure_directory(archive_directory)
  archived_build_file = archived_build_file_template % build.tuple()
  if not os.path.exists(archived_build_file):
    download_file(hosted_build_url_template % build.commit, archived_build_file)
  return archived_build_file

def ensure_build_file(build):
  ensure_directory(extraction_directory)
  extracted_build_file = extracted_build_file_template % build.tuple()
  if not os.path.exists(extracted_build_file):
    archived_build_file = ensure_archived_build_file(build)
    extract_file(archived_build_file, archived_build_file_inner_path, extracted_build_file)
  return extracted_build_file

def main():
  args = parse_argsets([build_args])
  build_file = ensure_build_file(Build(args.datetime, args.commit))
  print('Build file: ', build_file)

if __name__ == '__main__':
  main()
