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
import re
import sys

from constants import datetime_re

def parse_argsets(argsets, parser=None):
  if not parser:
    parser = argparse.ArgumentParser()
  for argset in argsets:
    argset.add_args(parser)
  args = parser.parse_args()
  for argset in argsets:
    argset.validate_args(parser, args)
  return args

def fail(parser, message):
  print(message)
  parser.print_help()
  sys.exit(1)

class build_args(object):
  @staticmethod
  def add_args(parser):
    parser.add_argument('--datetime', type=str, help='The datetime to associate with the build.')
    parser.add_argument('--commit', type=str, help='The build commit to download.')

  @staticmethod
  def validate_args(parser, args):
    if not (args.datetime and re.match(datetime_re, args.datetime)):
      fail(parser, '--datetime invalid.')
    if not args.commit:
      fail(parser, '--commit missing.')

class chromium_src_arg(object):
  @staticmethod
  def add_args(parser):
    parser.add_argument('--chromium-src', type=str, help='The path to the Chromium src directory.')

  @staticmethod
  def validate_args(parser, args):
    if not args.chromium_src:
      fail(parser, '--chromium-src missing.')

class device_arg(object):
  @staticmethod
  def add_args(parser):
    parser.add_argument('--device', type=str, default=None, help='The device serial ID to deploy to.')

  @staticmethod
  def validate_args(parser, args):
    pass

class step_arg(object):
  @staticmethod
  def add_args(parser):
    parser.add_argument('--step', type=str, default='every', help='The amount to step with each build, must be one of [every|daily|weekly]. Defaults to every.')

  @staticmethod
  def validate_args(parser, args):
    if args.step not in ['every', 'daily', 'weekly']:
      fail(parser, '--step invalid.')

class page_filter_arg(object):
  @staticmethod
  def add_args(parser):
    parser.add_argument('--page-filter', type=str, default=None, help='Optional page filter to pass to run-big-benchmarks')

  @staticmethod
  def validate_args(parser, args):
    pass
