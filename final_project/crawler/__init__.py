# web crawler
import pathlib

import click

from crawler.crawl import crawl


@click.command("Crawler")
@click.argument("url")
@click.argument("storage_directory")
def main(url: str, storage_directory: str):
    crawl(url, pathlib.Path(storage_directory))


def __main__():
    main()
