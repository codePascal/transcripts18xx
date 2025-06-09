#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess


def main():
    update()
    build()


def update():
    subprocess.run(
        ['sphinx-apidoc', '-o', './docs/source', './transcripts18xx']
    )


def build():
    subprocess.run(
        ['sphinx-build', '-M', 'html', './docs/source', './docs/build'],
        check=True
    )


if __name__ == '__main__':
    main()
