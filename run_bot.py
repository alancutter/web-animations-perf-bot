#! /usr/bin/python

from __future__ import division
from __future__ import print_function

import argparse
import time
import sys

from build import Build
from list_builds import list_daily_builds
from get_build import ensure_build_file
from deploy_build import deploy_build
from common_args import parse_argsets, chromium_src_arg

from constants import (
  datetime_format,
  default_seconds_between_polls,
)


def test_build(chromium_src, build, device):
  build_file = ensure_build_file(build)
  deploy_build(build_file, device)
  results_file = run_benchmarks(chromium_src, build)
  upload_results(chromium_src, results_file)

def get_command_line_args():
  now = time.strftime(datetime_format)
  parser = argparse.ArgumentParser()
  parser.add_argument('--seconds-between-polls', type=int, default=default_seconds_between_polls, help='How long to wait between batches of runs inclusive of the time taken to execute the batch.')
  parser.add_argument('--from-datetime', type=str, default=now, help='The earliest datetime for pulling Android builds. Defaults to now: %s' % now)
  parser.add_argument('--device', type=str, default=None, help='The serial ID of an Android device to run the tests on.')
  return parse_argsets(parser, [chromium_src_arg])

def main():
  args = get_command_line_args()
  last_tested_datetime = args.from_datetime
  while True:
    next_poll_time = time.time() + args.seconds_between_polls
    untested_builds = [build for build in list_daily_builds() if build.datetime > last_tested_datetime]
    for i, build in enumerate(untested_builds):
      print('Testing build %s of %s:\n%s' % (i + 1, len(untested_builds), build))
      test_build(args.chromium_src, build, args.device)
    sleep_seconds = int(next_poll_time - time.time())
    if sleep_seconds > 0:
      print('Sleeping for %s seconds (%s minutes)' % (sleep_seconds, sleep_seconds / 60))
      time.sleep(sleep_seconds)
    else:
      print('No time for sleeping!')

if __name__ == '__main__':
  main()
