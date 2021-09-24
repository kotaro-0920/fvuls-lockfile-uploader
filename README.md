# Python Container Action Template

[![Action Template](https://img.shields.io/badge/Action%20Template-Python%20Container%20Action-blue.svg?colorA=24292e&colorB=0366d6&style=flat&longCache=true&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAM6wAADOsB5dZE0gAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAERSURBVCiRhZG/SsMxFEZPfsVJ61jbxaF0cRQRcRJ9hlYn30IHN/+9iquDCOIsblIrOjqKgy5aKoJQj4O3EEtbPwhJbr6Te28CmdSKeqzeqr0YbfVIrTBKakvtOl5dtTkK+v4HfA9PEyBFCY9AGVgCBLaBp1jPAyfAJ/AAdIEG0dNAiyP7+K1qIfMdonZic6+WJoBJvQlvuwDqcXadUuqPA1NKAlexbRTAIMvMOCjTbMwl1LtI/6KWJ5Q6rT6Ht1MA58AX8Apcqqt5r2qhrgAXQC3CZ6i1+KMd9TRu3MvA3aH/fFPnBodb6oe6HM8+lYHrGdRXW8M9bMZtPXUji69lmf5Cmamq7quNLFZXD9Rq7v0Bpc1o/tp0fisAAAAASUVORK5CYII=)](https://github.com/jacobtomlinson/python-container-action)
[![Actions Status](https://github.com/futurevuls/fvuls-lockfile-uploader/workflows/Lint/badge.svg)](https://github.com/futurevuls/fvuls-lockfile-uploader/actions)
[![Actions Status](https://github.com/futurevuls/fvuls-lockfile-uploader/workflows/Integration%20Test/badge.svg)](https://github.com/futurevuls/fvuls-lockfile-uploader/actions)

This action can be used for uploading your lockfiles to future-vuls through the Public API.

## Usage

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `path`  | Relative path to lockfile |
| `repoName` _(optional)_  | Specify a prefix for path ex|

## Examples

### Using the optional input

This is how to use the optional input.

```yaml
with:
  repoName: ${{ github.repository }} # this is optional
  path: './go.sum' # relative path to lockfile
```

### Final Working Example

The example below will upload `go.sum` and `./web/yarn.lock`
and the Action will only run when changes are applied to these files and pushed to release.

```yaml
on:
  push:
    # Run Action only when changes are applied to these files and pushed to release.
    paths:
      - 'go.sum'
      - './web/yarn.lock'
    branches:
      - release

name: Check lockfiles
jobs:
  build:
    env:
      FVULS_SERVER_UUID: ${{ secrets.FVULS_SERVER_UUID }} # change me
      FVULS_TOKEN: ${{ secrets.FVULS_TOKEN }} # change me
    name: Upload lockfile
    runs-on: ubuntu-20.04
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0
      - name: Upload go.sum
        uses: futurevuls/fvuls-lockfile-uploader@main 
        with:
          repoName: ${{ github.repository }}
          path: './go.sum'
      - name: Upload web/yarn.lock
        uses: futurevuls/fvuls-lockfile-uploader@main 
        with:
          repoName: ${{ github.repository }}
          path: './web/yarn.lock'

```