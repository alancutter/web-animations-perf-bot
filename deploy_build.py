#! /usr/bin/python

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
  args = parse_argsets(parser, [device_arg])
  if not args.apk:
    print('No build file APK specified.')
    parser.print_help()
    sys.exit(1)
  deploy_build(args.apk, args.device)

if __name__ == '__main__':
  main()
