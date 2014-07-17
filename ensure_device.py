#! /usr/bin/python

from __future__ import division
from __future__ import print_function

import argparse
import subprocess

from common_args import parse_argsets, device_arg


def get_connected_devices():
  return [line.split()[0]
    for line in subprocess.check_output(['adb', 'devices']).split('\n')
    if len(line.split()) == 2]

def ensure_device(preferred_device):
  while True:
    devices = get_connected_devices()
    if preferred_device in devices:
      return preferred_device
    if preferred_device:
      print('Device %s not attached' % preferred_device)
    if len(devices) > 0:
      for i, device in enumerate(devices):
        if raw_input('Use connected device %s [%s of %s]? (y/[n]): ' % (device, i + 1, len(devices))) == 'y':
          return device
    else:
      print('Waiting for device to be attached')
      subprocess.check_call(['adb', 'wait-for-devices'])

def main():
  args = parse_argsets([device_arg])
  print('Device:', ensure_device(args.device))

if __name__ == '__main__':
  main()
