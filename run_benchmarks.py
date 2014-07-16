#! /usr/bin/python

from __future__ import print_function

import argparse

from constants import (
  android_device_id,
  datetime_format,
  seconds_between_polls,
)


def run_benchmarks(chromium_src, build):
  results_file = results_file_template % build.tuple()

def get_command_line_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--chromium-src', type=str, help='The path to the Chromium src directory.')
  parser.add_argument('--datetime', type=str, help='The datetime to associate with the build.')
  parser.add_argument('--commit', type=str, help='The build commit to download.')
  args = parser.parse_args()
  if not args.from_datetime:
    args.from_datetime = now
  if not args.chromium_src:
    print('--chromium-src missing.')
    parser.print_help()
    sys.exit(1)
  if not re.match(datetime_re, args.datetime):
    print('--datetime invalid.')
    parser.print_help()
    sys.exit(1)
  if not args.commit:
    print('--commit missing.')
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
