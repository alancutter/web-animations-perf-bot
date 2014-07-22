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
import os
import subprocess
import sys
import time

from build import Build
from common_args import parse_argsets, chromium_src_arg, device_arg, step_arg
from deploy_build import deploy_build
from ensure_device import ensure_device
from get_build import ensure_build_file
from list_builds import list_builds
from run_benchmarks import run_benchmarks
from upload_results import upload_results

from constants import (
  datetime_format,
  default_seconds_between_polls,
)


def test_build(chromium_src, build, device):
  build_file = ensure_build_file(build)
  print('Got the build file!')
  deploy_build(build_file, device)
  print('Deployed the build!')
  results_file = run_benchmarks(chromium_src, build, device)
  print('Got the results!')
  upload_results(chromium_src, results_file)
  print('Uploaded the results!')

def get_command_line_args():
  now = time.strftime(datetime_format)
  parser = argparse.ArgumentParser()
  parser.add_argument('--seconds-between-polls', type=int, default=default_seconds_between_polls, help='How long to wait between batches of runs inclusive of the time taken to execute each batch.')
  parser.add_argument('--from-datetime', type=str, default=now, help='The earliest datetime for pulling Android builds. Defaults to now: %s' % now)
  return parse_argsets([chromium_src_arg, device_arg, step_arg], parser)

def main():
  args = get_command_line_args()
  default_device = ensure_device(args.device) # Try to get any user interaction out of the way earlier rather than later.
  last_tested_datetime = args.from_datetime
  while True:
    next_poll_time = time.time() + args.seconds_between_polls
    untested_builds = list_builds(args.step, last_tested_datetime)
    for i, build in enumerate(untested_builds):
      print('Testing build %s of %s:\n%s' % (i + 1, len(untested_builds), build))
      default_device = ensure_device(default_device)
      test_build(args.chromium_src, build, default_device)
      last_tested_datetime = build.datetime
    sleep_seconds = int(next_poll_time - time.time())
    if sleep_seconds > 0:
      print('Sleeping for %s seconds (%s minutes)' % (sleep_seconds, sleep_seconds // 60))
      time.sleep(sleep_seconds)
    else:
      print('No time for sleeping!')

if __name__ == '__main__':
  main()
