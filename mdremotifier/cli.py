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
from typing import Dict, List, Optional, Set, Tuple, Union
from urllib.parse import ParseResult, urljoin, urlparse

import colorama
import mistletoe
from bs4 import BeautifulSoup
from mistletoe.markdown_renderer import (LinkReferenceDefinition,
                                         MarkdownRenderer)
from mistletoe.span_token import (HtmlSpan, Image, InlineCode, Link, RawText,
                                  SpanToken)
from mistletoe.token import Token
from rich.console import Console
from rich_argparse import RichHelpFormatter
from typing_extensions import Literal

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

  def __init__(self, link_url_prefix: str, img_url_prefix: str,
               all_references: bool, console: Console) -> None:
    self._link_url_prefix = link_url_prefix
    self._img_url_prefix = img_url_prefix
    self._all_references = all_references
    self._console = console
    self._seen_labels: Set[str] = set()
    self._label2type: Dict[str, Tuple[Literal['img', 'link'],
                                      Union[Link, Image]]] = {}

  def _ShouldReplaceURL(self, url: str) -> bool:
    url_pr: ParseResult = urlparse(url)
    if url_pr.scheme != '':
      return False
    if url_pr.path == '':
      return False
    return True

  def _ReplaceURL(self, url: str, *, is_img: bool) -> str:
    """Replace the URL with a raw.githubusercontent.com URL if it is a relative
      path to a file in the repository."""
    if self._ShouldReplaceURL(url):
      url_prefix = (self._img_url_prefix if is_img else self._link_url_prefix)
      # new_url = f'{self._url_prefix}{url_pr.path.lstrip("/")}'
      new_url = urljoin(url_prefix, url)
      self._console.print(f'{url} -> {new_url}')
      return new_url
    return url

  def _UpdateBS4Image(self, img: BeautifulSoup) -> bool:
    if 'src' not in img.attrs:
      return False
    src0 = img.attrs['src']
    if not isinstance(src0, str):
      raise TypeError(f"Expected 'src' to be a string, but got {type(src0)}")
    new_src = self._ReplaceURL(src0, is_img=True)
    if new_src == src0:
      return False
    img.attrs['src'] = new_src
    return True

  def _SetLabelType(self, *, token: Union[Image, Link], label: str,
                    link_type: Literal['img', 'link']):
    self._seen_labels.add(label)
    if label not in self._label2type:
      self._label2type[label] = (link_type, token)
    else:
      prev_link_type, prev_token = self._label2type[label]
      if prev_link_type != link_type and self._img_url_prefix != self._link_url_prefix:
        self._console.print(
            f'Label "{label}" was previously used as a {prev_link_type}, but now as a {link_type}.'
        )
        raise ValueError(
            f'Label "{label}" was previously used as a {prev_link_type}, but now as a {link_type}.'
            ' This is not allowed when --img-url-prefix is set to a different value than --url-prefix.'
            f'\n token: {token}'
            f'\n prev_token: {prev_token}')

  def _UpdateText(self, token: SpanToken):
    """Update the text contents of a span token and its children.
      `InlineCode` tokens are left unchanged."""

    if isinstance(token, Image):
      if token.label is not None:
        self._SetLabelType(token=token, label=token.label, link_type='img')
      else:
        token.src = self._ReplaceURL(token.src, is_img=True)
    elif isinstance(token, Link):
      if token.label is not None:
        self._SetLabelType(token=token, label=token.label, link_type='link')
      else:
        token.target = self._ReplaceURL(token.target, is_img=False)
    elif isinstance(token, (LinkReferenceDefinition)):
      if self._all_references or token.label in self._seen_labels:
        prev_link_type, _ = self._label2type.get(token.label, (None, None))

        token.dest = self._ReplaceURL(token.dest,
                                      is_img=prev_link_type == 'img')
    elif isinstance(token, (RawText, HtmlSpan)):
      soup = BeautifulSoup(token.content, 'html.parser')
      updated = False
      for img in soup.find_all('img'):
        updated |= self._UpdateBS4Image(img)
      if updated:
        token.content = str(soup)
    else:
      pass

    if not isinstance(token, InlineCode) and hasattr(token, 'children'):
      children: Optional[List[Token]] = token.children  # type: ignore
      if children is not None:
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

    children: Optional[List[Token]] = token.children  # type: ignore
    if children is not None:
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
        ' Example: "https://github.com/realazthat/mdremotifier/blob/master/".')
    p.add_argument(
        '--img-url-prefix',
        type=str,
        required=False,
        default=None,
        help='URL prefix to replace the local URLs with, specifically for images.'
        ' Should probably end in a slash.'
        ' Example: "https://raw.githubusercontent.com/realazthat/mdremotifier/master/".'
        ' Defaults to the value of --url-prefix.')
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
    url_prefix: str = args.url_prefix
    img_url_prefix: str = url_prefix
    if args.img_url_prefix is not None:
      img_url_prefix = args.img_url_prefix

    with MarkdownRenderer() as renderer:
      doc = mistletoe.Document(_GetInput(args))
      updater = _Updater(link_url_prefix=url_prefix,
                         img_url_prefix=img_url_prefix,
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
