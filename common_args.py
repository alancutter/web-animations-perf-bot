from __future__ import print_function

import sys

class ArgSet(object):
  def __init__(self, add_args, validate_args):
    self.add_args = add_args
    self.validate_args = validate_args

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

build_args = ArgSet(
  add_args = lambda parser: (
    parser.add_argument('--datetime', type=str, help='The datetime to associate with the build.'),
    parser.add_argument('--commit', type=str, help='The build commit to download.'),
  ),
  validate_args = lambda parser, args: (
    () if re.match(datetime_re, args.datetime) else (
      fail(parser, '--datetime invalid.'),
    ),
    () if args.commit else (
      fail(parser, '--commit missing.'),
    ),
  ),
)

chromium_src_arg = ArgSet(
  add_args = lambda parser: (
    parser.add_argument('--chromium-src', type=str, help='The path to the Chromium src directory.'),
  ),
  validate_args = lambda parser, args: (
    () if args.chromium_src else (
      fail(parser, '--chromium-src missing.'),
    ),
  ),
)
