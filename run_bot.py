#! /usr/bin/python

from __future__ import division
from __future__ import print_function

import argparse
import time

from build import Build
from list_builds import list_daily_builds
from get_build import ensure_build_file

from constants import (
  android_device_id,
  datetime_format,
  seconds_between_polls,
)


def test_build(build, chromium_src):
  build_file = ensure_build_file(build)
  deploy_build(build_file, android_device_id)
  results_file = run_benchmarks(chromium_src, build)
  upload_results(chromium_src, results_file)

def get_command_line_args():
  now = time.strftime(datetime_format)
  parser = argparse.ArgumentParser()
  parser.add_argument('--from-datetime', type=str, help='The earliest datetime for pulling Android builds. Defaults to now: %s' % now)
  parser.add_argument('--chromium-src', type=str, help='The path to the Chromium src directory.')
  args = parser.parse_args()
  if not args.from_datetime:
    args.from_datetime = now
  if not args.chromium_src:
    print('--chromium-src missing')
    parser.print_help()
    sys.exit(1)
  return args

def main():
  args = get_command_line_args()
  last_tested_datetime = args.from_datetime
  while True:
    next_poll_time = time.time() + seconds_between_polls
    untested_builds = [build for build in list_daily_builds() if build.datetime > last_tested_datetime]
    for i, build in enumerate(untested_builds):
      print('Testing build %s of %s:\n%s' % (i + 1, len(untested_builds), build))
      test_build(build, chromium_src)
    sleep_seconds = int(next_poll_time - time.time())
    if sleep_seconds > 0:
      print('Sleeping for %s seconds (%s minutes)' % (sleep_seconds, sleep_seconds / 60))
      time.sleep(sleep_seconds)

if __name__ == '__main__':
  main()
