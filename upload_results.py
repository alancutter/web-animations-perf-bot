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

from __future__ import print_function

import argparse
import json
import os
import re
import sys
import time
import urllib
import urllib2

from constants import (
  results_filename_re,
  spreadsheet_url,
  unwanted_test,
  upload_datetime_format,
  wanted_smoothness_tests,
)


def test_filter(test, wanted_tests = None):
  if test.startswith(unwanted_test):
    return False
  if wanted_tests and not any(test.startswith(prefix) for prefix in wanted_tests):
    return False
  return True

def get_metrics(test_results):
  if '_BlinkPerfMeasurement' in test_results:
    metrics = test_results['_BlinkPerfMeasurement']['metrics']
    metrics = {test: metrics[test] for test in metrics if test_filter(test)}
    metrics = {(test[:test.index('.')] if '.' in test else test): metrics[test] for test in metrics}
  elif 'smoothness.perf_week.perf_week' in test_results:
    metrics = test_results['smoothness.perf_week.perf_week']['metrics']
    metrics = {test: metrics[test] for test in metrics if test_filter(test, wanted_smoothness_tests)}
  else:
    raise Exception('Unknown measurement: ' + str(test_results.keys()))
  return metrics

def retry_loop(f):
  wait = 1
  while True:
    try:
      f()
      return
    except Exception:
      print(sys.exc_info()[1])
      print('Retrying in %s second(s)...' % wait)
      time.sleep(wait)
      wait *= 2


def upload_results(path):
  print('Uploading results file: %s' % path)
  commit_date, commit, device, username = re.match(results_filename_re, os.path.basename(path)).groups()
  run_timestamp = time.strftime(upload_datetime_format, time.gmtime(os.stat(path).st_mtime))
  results_blob = json.loads(re.search('<script id="results-json" type="application/json">(.*?)</script>', open(path).read()).group(1))
  metrics = get_metrics(results_blob[0]['tests'])
  for i, test in enumerate(metrics):
    print('[%s of %s] Uploading results for %s' % (i + 1, len(metrics), test))
    post_data = urllib.urlencode({
      'test': test,
      'commit': commit,
      'commit_date': commit_date,
      'run_timestamp': run_timestamp,
      'username': username,
      'device': device,
      'results': ','.join(map(str, metrics[test]['current'])),
      'unit': metrics[test]['units'],
    })
    print(post_data)
    # FIXME: Upload all the test results in one batch.
    retry_loop(lambda: urllib2.urlopen(spreadsheet_url, post_data))

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--results-file', action='append', help='Path to results file with the filename format: results_<commit_datetime>_<commit>_<device>_<username>.html')
  args = parser.parse_args()
  if not args.results_file:
    print('--results-file missing.')
    parser.print_help()
    sys.exit(1)
  for result in args.results_file:
    upload_results(result)

if __name__ == '__main__':
  main()
