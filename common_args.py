from __future__ import print_function

import re
import sys

from constants import datetime_re

def parse_argsets(parser, argsets):
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
    if not re.match(datetime_re, args.datetime):
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
