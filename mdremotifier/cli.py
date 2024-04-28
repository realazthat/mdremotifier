# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
#
# The mdremotifier project requires contributions made to this file be licensed
# under the MIT license or a compatible open source license. See LICENSE.md for
# the license text.
"""
README.md: Change local {links,images} to remote.
"""
import argparse
import logging
import sys
import warnings
from pathlib import Path
from shutil import get_terminal_size
from typing import Dict, List, Optional
from urllib.parse import ParseResult, urljoin, urlparse

import colorama
import mistletoe
from bs4 import BeautifulSoup
from mistletoe.markdown_renderer import (LinkReferenceDefinition,
                                         MarkdownRenderer)
from mistletoe.span_token import HtmlSpan, Image, InlineCode, Link, SpanToken
from mistletoe.token import Token
from rich.console import Console
from rich_argparse import RichHelpFormatter

from . import _build_version

logger = logging.getLogger(__name__)


def _GetProgramName() -> str:
  if __package__:
    # Use __package__ to get the base package name
    base_module_path = __package__
    # Infer the module name from the file path, with assumptions about the structure
    module_name = Path(__file__).stem
    # Construct what might be the intended full module path
    full_module_path = f'{base_module_path}.{module_name}' if base_module_path else module_name
    return f'python -m {full_module_path}'
  else:
    return sys.argv[0]


class _CustomRichHelpFormatter(RichHelpFormatter):

  def __init__(self, *args, **kwargs):
    if kwargs.get('width') is None:
      width, _ = get_terminal_size()
      if width == 0:
        warnings.warn('Terminal width was set to 0, using default width of 80.',
                      RuntimeWarning,
                      stacklevel=0)
        # This is the default in get_terminal_size().
        width = 80
      # This is what HelpFormatter does to the width returned by
      # `get_terminal_size()`.
      width -= 2
      kwargs['width'] = width
    super().__init__(*args, **kwargs)


def _GetInput(args: argparse.Namespace) -> str:
  path_str = args.input
  if path_str == '-':
    return sys.stdin.read()

  path = Path(path_str)
  if not path.exists():
    raise FileNotFoundError(f'File not found: {path_str}')

  with path.open() as fin:
    return fin.read()


def _DumpOutput(args: argparse.Namespace, output: str):
  path_str = args.output
  if path_str == '-':
    sys.stdout.write(output)
    return

  path = Path(path_str)
  with path.open('w') as fout:
    fout.write(output)


class _Updater:

  def __init__(self, url_prefix: str, all_references: bool,
               console: Console) -> None:
    self._url_prefix = url_prefix
    self._all_references = all_references
    self._console = console
    self._label2token: Dict[str, Token] = {}

  def _ShouldReplaceURL(self, url: str) -> bool:
    url_pr: ParseResult = urlparse(url)
    if url_pr.scheme != '':
      return False
    if url_pr.path == '':
      return False
    return True

  def _ReplaceURL(self, url: str) -> str:
    """Replace the URL with a raw.githubusercontent.com URL if it is a relative
      path to a file in the repository."""
    if self._ShouldReplaceURL(url):
      # new_url = f'{self._url_prefix}{url_pr.path.lstrip("/")}'
      new_url = urljoin(self._url_prefix, url)
      self._console.print(f'{url} -> {new_url}')
      return new_url
    return url

  def _UpdateText(self, token: SpanToken):
    """Update the text contents of a span token and its children.
      `InlineCode` tokens are left unchanged."""

    if isinstance(token, Image):
      if token.label is not None:
        self._label2token[token.label] = token
      else:
        token.src = self._ReplaceURL(token.src)
    elif isinstance(token, Link):
      if token.label is not None:
        self._label2token[token.label] = token
      else:
        token.target = self._ReplaceURL(token.target)
    elif isinstance(token, HtmlSpan):
      if token.content.startswith('<img '):
        # parse the img html
        img = BeautifulSoup(token.content, 'html.parser')
        src0 = img['src']
        if not isinstance(src0, str):
          raise TypeError(
              f"Expected 'src' to be a string, but got {type(src0)}")
        new_src = self._ReplaceURL(src0)
        if new_src != src0:
          img['src'] = new_src
          token.content = str(img)
    elif isinstance(token, (LinkReferenceDefinition)):
      if self._all_references or token.label in self._label2token:
        token.dest = self._ReplaceURL(token.dest)
    else:
      pass

    if not isinstance(token, InlineCode) and hasattr(token, 'children'):
      children: List[Token] = token.children  # type: ignore
      for child in children:
        if not isinstance(child, SpanToken):
          logger.error(f'Expected SpanToken, but got {type(child)}')
          continue
        self._UpdateText(child)

  def Update(self, token: Token):
    """Update the text contents of paragraphs and headings within this block,
      and recursively within its children."""

    if isinstance(token, (SpanToken)):
      self._UpdateText(token)

    if not hasattr(token, 'children'):
      return

    children: List[Token] = token.children  # type: ignore
    for child in children:
      self.Update(child)


def main():
  console = Console(file=sys.stderr)
  args: Optional[argparse.Namespace] = None
  try:
    # Windows<10 requires this.
    colorama.init()
    p = argparse.ArgumentParser(prog=_GetProgramName(),
                                description=__doc__,
                                formatter_class=_CustomRichHelpFormatter)

    p.add_argument('-i',
                   '--input',
                   dest='input',
                   type=str,
                   required=True,
                   help='Input markdown file, use "-" for stdin.')
    p.add_argument('-o',
                   '--output',
                   dest='output',
                   type=str,
                   required=True,
                   help='Output markdown file, use "-" for stdout.')
    p.add_argument(
        '--url-prefix',
        type=str,
        required=True,
        help='URL prefix to replace the local URLs with.'
        ' Should probably end in a slash.'
        ' Example: "https://raw.githubusercontent.com/realazthat/mdremotifier/master/".'
    )
    p.add_argument(
        '--all-references',
        action='store',
        default=False,
        help=
        'Should all references be updated be externalized, or only those that are used by links and images?'
    )
    p.add_argument('--version',
                   action='version',
                   version=_build_version,
                   help='Show the version and exit.')

    args = p.parse_args()

    with MarkdownRenderer() as renderer:
      doc = mistletoe.Document(_GetInput(args))
      updater = _Updater(url_prefix=args.url_prefix,
                         all_references=args.all_references,
                         console=console)
      updater.Update(doc)
      # Two passes, in case the linked reference came first.
      updater.Update(doc)
      _DumpOutput(args, renderer.render(doc))

  except Exception:
    console.print_exception()
    if args:
      console.print('args:', args._get_kwargs(), style='bold red')

    sys.exit(1)
    return


if __name__ == '__main__':
  main()
