#! /usr/bin/python

from __future__ import print_function

import argparse
import os
import subprocess

from common_args import parse_argsets, chromium_src_arg, build_args, device_arg
from build import Build

from constants import (
  run_benchmark_script,
  results_directory,
  results_file_template,
)


def run_benchmarks(chromium_src, build, device):
  if not os.path.exists(results_directory):
    os.mkdir(results_directory)
  results_file = results_file_template % build.tuple()
  command = ['python', run_benchmark_script, '--browser', 'android-content-shell', '--page-filter', 'css-animations-simultaneous-by-updating-class', '--output', os.path.abspath(results_file)]
  if device:
    command.extend(['--device', device])
  print('Executing:', ' '.join(command))
  print('Using working directory:', chromium_src)
  subprocess.check_call(command, cwd=chromium_src)

def main():
  args = parse_argsets(argparse.ArgumentParser(), [chromium_src_arg, build_args, device_arg])
  results_file = run_benchmarks(args.chromium_src, Build(args.datetime, args.commit), args.device)
  print('Results file:', results_file)

if __name__ == '__main__':
  main()
