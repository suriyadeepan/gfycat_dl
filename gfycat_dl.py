import requests
import argparse
import wget
import os

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(
    description='gfycat_dl : Download anything from gfycat'
    )
parser.add_argument('url', type=str, help="URL")
parser.add_argument('--format', type=str, default='mp4',
    help='Download format (mp4/webm)')
parser.add_argument('--dir', type=str, default='.',
    help='Download path')

# parse command-line arguments
args = parser.parse_args()


def parse(url, vid_format='mp4'):
  sources = BeautifulSoup(requests.get(url).content,
      features='html.parser').find_all('source')
  for source in sources:
    if 'src' in source.attrs:
      if f'.{vid_format}' in source['src'] and 'mobile' not in source['src']:
        return source.get('src')


def download(url, vid_format='mp4', save_to='.'):
  res_url = parse(url, vid_format)
  filepath = os.path.join(save_to, res_url.split('/')[-1])
  wget.download(res_url, filepath)
  print(f'\n\nSaved to [{filepath}]')


if __name__ == '__main__':
  if not os.path.exists(args.dir):
    os.mkdir(args.dir)

  download(args.url, args.format, args.dir)
