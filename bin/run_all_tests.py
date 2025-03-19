#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from pathlib import Path

if __name__ == '__main__':
    loader = unittest.TestLoader()
    test_dir = Path(__file__).parent.parent.joinpath('tests')
    print(test_dir)
    suite = loader.discover(test_dir.__str__())
    runner = unittest.TextTestRunner()
    runner.run(suite)
