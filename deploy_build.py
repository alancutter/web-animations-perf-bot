#! /usr/bin/python

from __future__ import print_function

import argparse
import sys
import subprocess


def deploy_build(apk, device_id=None):
  print('Deploying\n\t%s\nto android device %s' % (apk, device_id if device_id else ''))
  command = ['adb', 'install', '-r', apk]
  if device_id:
    command.insert(1, '-s')
    command.insert(2, device_id)
  print('Executing\n\t%s\n...' % ' '.join(command), end='')
  output = subprocess.check_output(command)
  print('done')
  print(output)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--apk', type=str, help='The path to the build file APK to deploy.')
  parser.add_argument('--device', type=str, default=None, help='The device serial ID to deploy to.')
  args = parser.parse_args()
  if not args.apk:
    print('No build file APK specified.')
    parser.print_help()
    sys.exit(1)
  deploy_build(args.apk, args.device)

if __name__ == '__main__':
  main()
