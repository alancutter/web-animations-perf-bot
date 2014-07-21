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
import sys
import subprocess

from common_args import parse_argsets, device_arg


def deploy_build(apk, device_id=None):
  print('Deploying\n\t%s\nto android device %s' % (apk, device_id if device_id else ''))
  command = ['adb', 'install', '-r', apk]
  if device_id:
    command.insert(1, '-s')
    command.insert(2, device_id)
  print('Executing\n\t%s\n...' % ' '.join(command), end='')
  subprocess.check_call(command)
  print('done')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--apk', type=str, help='The path to the build file APK to deploy.')
  args = parse_argsets([device_arg], parser)
  if not args.apk:
    print('No build file APK specified.')
    parser.print_help()
    sys.exit(1)
  deploy_build(args.apk, args.device)

if __name__ == '__main__':
  main()
