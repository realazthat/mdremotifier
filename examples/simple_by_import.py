# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
#
# The mdremotifier project requires contributions made to this file be licensed
# under the MIT license or a compatible open source license. See LICENSE.md for
# the license text.


# SNIPPET_START
from rich.console import Console

from mdremotifier.mdremotifier import Render

md = """
# Example markdown file

## Local link

[LICENSE.md](./LICENSE.md).

## Local image

![local image](./img.png).
"""
url_prefix = 'https://github.com/realazthat/mdremotifier/blob/master/'
img_url_prefix = 'https://raw.githubusercontent.com/realazthat/mdremotifier/master/'

console = Console()
print(
    Render(md=md,
           url_prefix=url_prefix,
           img_url_prefix=img_url_prefix,
           all_references=True,
           console=console))

# SNIPPET_END
