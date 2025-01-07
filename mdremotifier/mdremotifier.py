# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
#
# The mdremotifier project requires contributions made to this file be licensed
# under the MIT license or a compatible open source license. See LICENSE.md for
# the license text.

import logging
from typing import Dict, List, Optional, Set, Tuple, Union
from urllib.parse import ParseResult, urljoin, urlparse

import mistletoe
from bs4 import BeautifulSoup
from mistletoe.markdown_renderer import (LinkReferenceDefinition,
                                         MarkdownRenderer)
from mistletoe.span_token import (HtmlSpan, Image, InlineCode, Link, RawText,
                                  SpanToken)
from mistletoe.token import Token
from rich.console import Console
from typing_extensions import Literal

logger = logging.getLogger(__name__)


def Render(*, md: str, url_prefix: str, img_url_prefix: str,
           all_references: bool, console: Optional[Console]) -> str:
  """ Render the markdown with the given URL prefixes.

  Args:
    md: The markdown string to render.
    url_prefix: The URL prefix to replace the local URLs with.
      Should probably end in a slash.
      Example: "https://github.com/realazthat/mdremotifier/blob/master".
    img_url_prefix: The URL prefix to replace the local URLs with, specifically for images.
      Should probably end in a slash.
      Example: "https://raw.githubusercontent.com/realazthat/mdremotifier/master".
    all_references: Should all references be updated be externalized, or only those that are used by links and images?
    console: The console to print debug information to.
  """

  with MarkdownRenderer() as renderer:
    doc = mistletoe.Document(md)
    updater = Updater(link_url_prefix=url_prefix,
                      img_url_prefix=img_url_prefix,
                      all_references=all_references,
                      console=console)
    updater.Update(doc)
    # Two passes, in case the linked reference came first.
    updater.Update(doc)
    return renderer.render(doc)


class Updater:

  def __init__(self, link_url_prefix: str, img_url_prefix: str,
               all_references: bool, console: Optional[Console]) -> None:
    self._link_url_prefix = link_url_prefix
    self._img_url_prefix = img_url_prefix
    self._all_references = all_references
    self._console: Optional[Console] = console
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
      if self._console is not None:
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
        if self._console is not None:
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
