#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
import subprocess

from pathlib import Path


def main():
    update_resources()
    update()
    build()


def update_resources():
    # Update the resources linked in the README.md in the documentation folder.
    source = Path('tests/resources')
    target = Path('docs/source/_static')
    files = [
        '1830_201210_final.csv',
        '1830_201210_metadata.json',
        '1830_201210_states.json',
        '1830_201210_serialized.json',
        '1830_201210_flattened.csv'
    ]
    for file in files:
        shutil.copy(source.joinpath(file), target.joinpath(file))


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
