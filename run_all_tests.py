#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import subprocess


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Run tests')
    parser.add_argument('--coverage', action='store_true', help='Coverage')
    return parser.parse_args()


def run_tests() -> None:
    print('Running pytest...')
    subprocess.run(['pytest', 'tests/', '--disable-warnings'], check=True)


def run_tests_with_coverage() -> None:
    print('Running tests with coverage...')
    subprocess.run(['coverage', 'run', '-m', 'pytest', 'tests/'], check=True)

    print('Generating coverage report...')
    subprocess.run(['coverage', 'report', '-m'], check=True)

    print('Saving HTML coverage report to ./htmlcov/index.html...')
    subprocess.run(['coverage', 'html'], check=True)


if __name__ == '__main__':
    args = parse_arguments()
    if args.coverage:
        run_tests_with_coverage()
    else:
        run_tests()
