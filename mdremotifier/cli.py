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
import sys
import warnings
from pathlib import Path
from shutil import get_terminal_size
from typing import Optional

import colorama
from rich.console import Console
from rich_argparse import RichHelpFormatter

from . import _build_version, mdremotifier


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
        action='store_true',
        default=True,
        help=
        'Should all references be updated be externalized, or only those that are actually used by links and images?'
    )
    p.add_argument('--version',
                   action='version',
                   version=_build_version,
                   help='Show the version and exit.')

    args = p.parse_args()
    url_prefix: str = args.url_prefix
    img_url_prefix: str = url_prefix
    all_references: bool = args.all_references
    if args.img_url_prefix is not None:
      img_url_prefix = args.img_url_prefix

    _DumpOutput(
        args,
        mdremotifier.Render(md=_GetInput(args),
                            url_prefix=url_prefix,
                            img_url_prefix=img_url_prefix,
                            all_references=all_references,
                            console=console))
  except Exception:
    console.print_exception()
    if args:
      console.print('args:', args._get_kwargs(), style='bold red')

    sys.exit(1)
    return


if __name__ == '__main__':
  main()
