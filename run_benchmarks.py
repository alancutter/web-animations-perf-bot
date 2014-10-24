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
import os
import subprocess

from common_args import (
  parse_argsets,
  build_args,
  chromium_src_arg,
  device_arg,
  page_filter_arg,
)
from build import Build

from constants import (
  all_results_directory,
  results_directory_template,
  results_filename,
  run_benchmark_script,
)


def ensure_directory(directory):
  if not os.path.exists(directory):
    os.mkdir(directory)

def run_benchmarks(chromium_src, build, device, page_filter):
  username = subprocess.check_output(['whoami']).strip()
  results_directory = results_directory_template % (build.datetime, build.commit, device, username)
  ensure_directory(all_results_directory)
  ensure_directory(results_directory)
  command = [
    'python',
    run_benchmark_script,
    '--browser=android-content-shell',
    '--output-dir=' + os.path.abspath(results_directory),
    '--reset-results'
  ]
  if device:
    command.append('--device=' + device)
  if page_filter:
    command.append('--page-filter=' + page_filter)
  print('Executing:', ' '.join(command))
  print('Using working directory:', chromium_src)
  subprocess.check_call(command, cwd=chromium_src)
  return os.path.join(results_directory, results_filename)

def main():
  args = parse_argsets([chromium_src_arg, build_args, device_arg, page_filter_arg])
  results_file = run_benchmarks(args.chromium_src, Build(args.datetime, args.commit), args.device, args.page_filter)
  print('Results file:', results_file)

if __name__ == '__main__':
  main()
