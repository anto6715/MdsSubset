#!/usr/bin/env python
import sys
import json
import pathlib

import click
import copernicusmarine


def format_dict(**input_dict):
    formatted_str = ""
    for key, value in input_dict.items():
        formatted_str += f"\t- {key}: {value}\n"
    return formatted_str


@click.group()
def main():
    pass


@main.command()
@click.argument('configuration_file')
def subset_json(configuration_file: str):
    """Read subset arguments from a json file and sequentially download them"""
    with open(configuration_file) as f:
        config = json.load(f)

    for subset_section in config:
        copernicus_subset(**subset_section)


@main.command()
@click.option('-o', '--output-directory', required=True, type=str, help='Output directory')
@click.option('-f', '--output-filename', required=True, type=str, help='Output filename')
@click.option('-i', '--dataset-id', required=True, type=str, help='Dataset Id')
@click.option('-v', '--variables', multiple=True, type=str, help='Variables to download')
@click.option('-x', '--minimum-longitude', type=float, help='Minimum longitude for the subset.')
@click.option('-X', '--maximum-longitude', type=float, help='Maximum longitude for the subset. ')
@click.option('-y', '--minimum-latitude', type=float,
              help='Minimum latitude for the subset. Requires a float within this range:  [-90<=x<=90]')
@click.option('-Y', '--maximum-latitude', type=float,
              help='Maximum latitude for the subset. Requires a float within this range:  [-90<=x<=90]')
@click.option('-z', '--minimum-depth', type=float,
              help='Minimum depth for the subset. Requires a float within this range:  [x>=0]')
@click.option('-Z', '--maximum-depth', type=float,
              help='Maximum depth for the subset. Requires a float within this range:  [x>=0]')
@click.option('-t', '--start-datetime', type=str, default=False,
              help='Start datetime as: %Y|%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S|%Y-%m-%dT%H:%M:%S.%fZ')
@click.option('-T', '--end-datetime', type=str, default=False,
              help='End datetime as: %Y|%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S|%Y-%m-%dT%H:%M:%S.%fZ')
@click.option('-g', '--dataset-version', type=str, default=None, help='Dataset version or tag')
@click.option('-n', '--username', type=str, default=None, help='Username')
@click.option('-w', '--password', type=str, default=None, help='Password')
@click.option('--disable-progress-bar', is_flag=True, default=False, help='To disable the progress bar')
@click.option('--force-download', is_flag=True, default=False, help="Don't ask permission to download")
def subset_manual(**kwargs):
    copernicus_subset(**kwargs)


def copernicus_subset(**subset_kwargs) -> pathlib.Path:
    """Wrapper to copernicusmarine.subset."""
    # download
    try:
        return copernicusmarine.subset(**subset_kwargs, )
    except TypeError as e:
        print(f'ERROR - {e} - Wrong configuration:', file=sys.stderr)
        print(format_dict(**subset_kwargs), file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
