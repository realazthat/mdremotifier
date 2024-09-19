<!--

WARNING: This file is auto-generated by snipinator. Do not edit directly.
SOURCE: `.github/README.md.jinja2`.

-->
<!--







-->

# <div align="center">![mdremotifier][1]</div>

<div align="center">

</div>

<div align="center">

<!-- Icons from https://lucide.dev/icons/users -->
<!-- Icons from https://lucide.dev/icons/laptop-minimal -->

![**Audience:** Developers][2] ![**Platform:** Linux][3]

</div>

<p align="center">
  <strong>
    <a href="#-features">🎇Features</a>
    &nbsp;&bull;&nbsp;
    <a href="#-installation">🏠Installation</a>
    &nbsp;&bull;&nbsp;
    <a href="#-usage">🚜Usage</a>
    &nbsp;&bull;&nbsp;
    <a href="#-command-line-options">💻CLI</a>
    &nbsp;&bull;&nbsp;
    <a href="#-examples">💡Examples</a>
  </strong>
</p>

<p align="center">
  <strong>
    <a href="#-requirements">✅Requirements</a>
    &nbsp;&bull;&nbsp;
    <a href="#-docker-image">🐳Docker</a>
  </strong>
</p>

<div align="center">

![Top language][4] [![GitHub License][5]][6] [![PyPI - Version][7]][8]
[![Python Version][9]][8]

**CLI to replace `./image.png` to `raw.githubusercontent.com` remote URL in
README.md**

</div>

---

<div align="center">

|                   | Status                      | Stable                    | Unstable                  |                    |
| ----------------- | --------------------------- | ------------------------- | ------------------------- | ------------------ |
| **[Master][10]**  | [![Build and Test][11]][12] | [![since tagged][13]][14] |                           | ![last commit][15] |
| **[Develop][16]** | [![Build and Test][17]][12] | [![since tagged][18]][19] | [![since tagged][20]][21] | ![last commit][22] |

</div>

---

<img src="./.github/demo.gif" alt="Demo" width="100%">

<div align="center">
  <img src="./.github/pypi-demo.png" alt="Example result on pypi" width="100%">
</div>

---

## ❔ What

What mdremotifier does:

Turn this ([./examples/SIMPLE.md](./examples/SIMPLE.md)):

<!---->
```md
# Example markdown file

## Local link

[LICENSE.md](./LICENSE.md).

## Local image

![local image](./img.png).

```
<!---->

Into this ([./examples/SIMPLE.remotified.md](./examples/SIMPLE.remotified.md)):

<!---->
```md
# Example markdown file

## Local link

[LICENSE.md](https://github.com/realazthat/mdremotifier/blob/master/LICENSE.md).

## Local image

![local image](https://raw.githubusercontent.com/realazthat/mdremotifier/master/img.png).

```
<!---->

This is useful for uploading `README.md` files to third-party sites, like the
npmjs.com registry, or pypi.org registry, because these registries will break
the local images in your README when displayed on their sites.

See <https://pypi.org/project/mdremotifier/>, notice how all of the images are
not broken.

## 🎇 Features

- 📷🔗📡🌐🖼️ Replace local URLs with raw.githubusercontent.com URLs.

## 🏠 Installation

```bash
# Install from pypi (https://pypi.org/project/mdremotifier/)
pip install mdremotifier

# Install from git (https://github.com/realazthat/mdremotifier)
pip install git+https://github.com/realazthat/mdremotifier.git@v0.5.0
```

## 🚜 Usage

Example README: ([./examples/SIMPLE.md](./examples/SIMPLE.md)):

<!---->
```md
# Example markdown file

## Local link

[LICENSE.md](./LICENSE.md).

## Local image

![local image](./img.png).

```
<!---->

Generating the README:

<!--

-->

```bash
# Using this command:
# View the template file.
cat "examples/SIMPLE.md"

python -m mdremotifier.cli  \
  -i "examples/SIMPLE.md" \
  --url-prefix https://github.com/realazthat/mdremotifier/blob/master/ \
  --img-url-prefix https://raw.githubusercontent.com/realazthat/mdremotifier/master/ \
  -o "examples/SIMPLE.remotified.md"

# View the remotified file.
cat "examples/SIMPLE.remotified.md"
```

Result:

<!---->
```md
# Example markdown file

## Local link

[LICENSE.md](https://github.com/realazthat/mdremotifier/blob/master/LICENSE.md).

## Local image

![local image](https://raw.githubusercontent.com/realazthat/mdremotifier/master/img.png).

```
<!---->

Full example:

<!---->
<img src=".github/README.simple_example.generated.svg" alt="Output of `bash ./snipinator/examples/simple_example.sh`" />
<!---->

## 💻 Command Line Options

<!---->
<img src=".github/README.help.generated.svg" alt="Output of `python -m mdremotifier.cli --help`" />
<!---->

## 💡 Examples

- mdremotifier's own `README`:
  - Original: [./README.md](./README.md).
  - Remotified: [./.github/README.remotified.md](./.github/README.remotified.md).
  - Generation script: [./scripts/generate-readme.sh](./scripts/generate-readme.sh).
- Example:
  - Original: [./examples/SIMPLE.md](./examples/SIMPLE.md).
  - Remotified: [./examples/SIMPLE.remotified.md](./examples/SIMPLE.remotified.md).
  - Generation script: [./examples/simple_example.sh](./examples/simple_example.sh).
- Projects using mdremotifier:
  - [realazthat/snipinator][23].
    - README: [snipinator/README.md][24].
    - Generation script: [snipinator/scripts/generate-readme.sh#L29][25].
    - Remotified: [snipinator/README.md][26].
  - [github.com/realazthat/excalidraw-brute-export-cli][27].
    - README: [excalidraw-brute-export-cli/README.md][28].
    - Generation script:
      [excalidraw-brute-export-cli/scripts/generate-readme.sh#L65][29].
    - Remotified: [excalidraw-brute-export-cli/README.md][30].

<!-- TODO: Rebuild this for mdremotifier

  - [github.com/realazthat/changeguard](https://github.com/realazthat/changeguard),
    See
    [changeguard/README.md.jinja2](https://github.com/realazthat/changeguard/blob/87d5104b52e651bb9195a3d46dd7f050acbcb534/README.md.jinja2).
  - [github.com/realazthat/comfy-catapult](https://github.com/realazthat/comfy-catapult),
    See
    [comfy-catapult/README.md.jinja2](https://github.com/realazthat/comfy-catapult/blob/ff353d48b25fa7b9c35fa11b31d5f2b3039c41c8/README.md.jinja2).
  - [github.com/realazthat/comfylowda](https://github.com/realazthat/comfylowda),
    See
    [comfylowda/README.md.jinja2](https://github.com/realazthat/comfylowda/blob/e01a32c38107aa0b89ccea21c4678d193a186a78/README.md.jinja2).
-->

## ✅ Requirements

- Linux-like environment
  - Why: Uses pexpect.spawn().
- Python 3.8+
  - Why: Some dev dependencies require Python 3.8+.

### Tested Platforms

- WSL2 Ubuntu 20.04, Python `3.8.0`.
- Ubuntu 20.04, Python `3.8.0, 3.9.0, 3.10.0, 3.11.0, 3.12.0`, tested in GitHub Actions
  workflow ([build-and-test.yml](./.github/workflows/build-and-test.yml)).

## 🐳 Docker Image

Docker images are published to [ghcr.io/realazthat/mdremotifier][31] at each
tag.

<!---->
```bash

# View the template file.
cat "examples/SIMPLE.md"

# Use the published images at ghcr.io/realazthat/mdremotifier.
# /data in the docker image is the working directory, so paths are simpler.
docker run --rm --tty \
  -v "${PWD}:/data" \
  ghcr.io/realazthat/mdremotifier:v0.5.0  \
  -i "examples/SIMPLE.md" \
  --url-prefix https://github.com/realazthat/mdremotifier/blob/master/ \
  --img-url-prefix https://raw.githubusercontent.com/realazthat/mdremotifier/master/ \
  -o "examples/SIMPLE.remotified.md"

# View the remotified file.
cat "examples/SIMPLE.remotified.md"


```
<!---->

If you want to build the image yourself, you can use the Dockerfile in the
repository.

<!---->
```bash

docker build -t my-mdremotifier-image .

# View the template file.
cat "examples/SIMPLE.md"

# /data in the docker image is the working directory, so paths are simpler.
docker run --rm --tty \
  -v "${PWD}:/data" \
  my-mdremotifier-image  \
  -i "examples/SIMPLE.md" \
  --url-prefix https://github.com/realazthat/mdremotifier/blob/master/ \
  --img-url-prefix https://raw.githubusercontent.com/realazthat/mdremotifier/master/ \
  -o "examples/SIMPLE.remotified.md"

# View the remotified file.
cat "examples/SIMPLE.remotified.md"


```
<!---->

## 🤏 Versioning

We use SemVer for versioning. For the versions available, see the tags on this
repository.

## 🔑 License

This project is licensed under the MIT License - see the
[./LICENSE.md](./LICENSE.md) file for details.

## 🙏 Thanks

Main libraries used in mdremotifier are:

- Markdown AST: [mistletoe](https://github.com/miyuchina/mistletoe).
- Colorful CLI help: [rich-argparse](https://github.com/hamdanal/rich-argparse).

## 🤝 Related Projects

Not complete, and not necessarily up to date. Make a PR
([contributions](#-contributions)) to insert/modify.

| Project                                           | Stars | Last Update  | Language | Platform | Similarity X Obviousness |
| ------------------------------------------------- | ----- | ------------ | -------- | -------- | ------------------------ |
| [bdashore3/remark-github-images][32]              | 0     | `2022/12/29` | JS       | CLI      | ⭐⭐⭐⭐⭐               |
| [laobie/WriteMarkdownLazily][33]                  | 36    | `2024/01/06` | Python   | CLI      | ⭐⭐⭐⭐                 |
| [crh19970307/mdul][34]                            | 1     | `2020/02/01` | Python   | CLI      | ⭐⭐⭐⭐                 |
| [SkyLee424/Go-MarkDown-Image-Transfer-Helper][35] | 0     | `2024/03/25` | Go       | CLI      | ⭐⭐⭐⭐                 |
| [jen6/imgo][36]                                   | 0     | `2020/03/18` | Pyhon    | CLI      | ⭐⭐⭐⭐                 |
| [chocoluffy/lazy-markdown][37]                    | 0     | `2016/11/20` | Python   | CLI      | ⭐⭐⭐⭐                 |
| [loheagn/gopic][38]                               | 0     | `2021/11/24` | Go       | CLI      | ⭐⭐⭐⭐                 |
| [Undertone0809/imarkdown][39]                     | 57    | `2024/01/06` | Python   | Python   | ⭐⭐⭐                   |
| [ravgeetdhillon/markdown-imgur-upload][40]        | 1     | `2022/03/26` | Python   | CLI      | ⭐⭐⭐                   |

## 🫡 Contributions

### Development environment: Linux-like

- For running `pre.sh` (Linux-like environment).

  - From [./.github/dependencies.yml](./.github/dependencies.yml), which is used for
    the GH Action to do a fresh install of everything:

    ```yaml
    bash: scripts.
    findutils: scripts.
    grep: tests.
    xxd: tests.
    git: scripts, tests.
    xxhash: scripts (changeguard).
    rsync: out-of-directory test.
    expect: for `unbuffer`, useful to grab and compare ansi color symbols.
    jq: dependency for [yq](https://github.com/kislyuk/yq), which is used to generate
      the README; the README generator needs to use `tomlq` (which is a part of `yq`)
      to query `pyproject.toml`.
    
    ```

  - Requires `pyenv`, or an exact matching version of python as in
    [./.python-version](./.python-version) (which is currently
    `3.8.0
`).
  - `jq`, ([installation](https://jqlang.github.io/jq/)) required for
    [yq](https://github.com/kislyuk/yq), which is itself required for our
    [./README.md](./README.md) generation, which uses `tomlq` (from the
    [yq](https://github.com/kislyuk/yq) package) to include version strings from
    [./pyproject.toml](./pyproject.toml).
  - act (to run the GH Action locally):
    - Requires nodejs.
    - Requires Go.
    - docker.
  - Generate animation:
    - docker
  - docker (for building the docker image).

### Commit Process

1. (Optionally) Fork the `develop` branch.
2. Stage your files: `git add path/to/file.py`.
3. `bash ./scripts/pre.sh`, this will format, lint, and test the code.
4. `git status` check if anything changed (generated
   [./README.md](./README.md) for example), if so, `git add` the
   changes, and go back to the previous step.
5. `git commit -m "..."`.
6. Make a PR to `develop` (or push to develop if you have the rights).

## 🔄🚀 Release Process

These instructions are for maintainers of the project.

1. In the `develop` branch, run `bash ./scripts/pre.sh` to ensure
   everything is in order.
2. In the `develop` branch, bump the version in
   [./pyproject.toml](./pyproject.toml), following semantic versioning
   principles. Also modify the `last_release` and `last_stable_release` in the
   `[tool.mdremotifier-project-metadata]` table as appropriate. Run
   `bash ./scripts/pre.sh` to ensure everything is in order.
3. In the `develop` branch, commit these changes with a message like
   `"Prepare release X.Y.Z"`. (See the contributions section
   [above](#commit-process)).
4. Merge the `develop` branch into the `master` branch:
   `git checkout master && git merge develop --no-ff`.
5. `master` branch: Tag the release: Create a git tag for the release with
   `git tag -a vX.Y.Z -m "Version X.Y.Z"`.
6. Publish to PyPI: Publish the release to PyPI with
   `bash ./scripts/deploy-to-pypi.sh`.
7. Push to GitHub: Push the commit and tags to GitHub with
   `git push && git push --tags`.
8. The `--no-ff` option adds a commit to the master branch for the merge, so
   refork the develop branch from the master branch:
   `git checkout develop && git merge master`.
9. Push the develop branch to GitHub: `git push origin develop`.

[1]: ./.github/logo-exported.svg
[2]:
  https://img.shields.io/badge/Audience-Developers-0A1E1E?style=plastic&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXVzZXJzIj48cGF0aCBkPSJNMTYgMjF2LTJhNCA0IDAgMCAwLTQtNEg2YTQgNCAwIDAgMC00IDR2MiIvPjxjaXJjbGUgY3g9IjkiIGN5PSI3IiByPSI0Ii8+PHBhdGggZD0iTTIyIDIxdi0yYTQgNCAwIDAgMC0zLTMuODciLz48cGF0aCBkPSJNMTYgMy4xM2E0IDQgMCAwIDEgMCA3Ljc1Ii8+PC9zdmc+
[3]:
  https://img.shields.io/badge/Platform-Linux-0A1E1E?style=plastic&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWxhcHRvcC1taW5pbWFsIj48cmVjdCB3aWR0aD0iMTgiIGhlaWdodD0iMTIiIHg9IjMiIHk9IjQiIHJ4PSIyIiByeT0iMiIvPjxsaW5lIHgxPSIyIiB4Mj0iMjIiIHkxPSIyMCIgeTI9IjIwIi8+PC9zdmc+
[4]:
  https://img.shields.io/github/languages/top/realazthat/mdremotifier.svg?&cacheSeconds=28800&style=plastic&color=0A1E1E
[5]:
  https://img.shields.io/github/license/realazthat/mdremotifier?style=plastic&color=0A1E1E
[6]: ./LICENSE.md
[7]:
  https://img.shields.io/pypi/v/mdremotifier?style=plastic&color=0A1E1E
[8]: https://pypi.org/project/mdremotifier/
[9]:
  https://img.shields.io/pypi/pyversions/mdremotifier?style=plastic&color=0A1E1E
[10]: https://github.com/realazthat/mdremotifier/tree/master
[11]:
  https://img.shields.io/github/actions/workflow/status/realazthat/mdremotifier/build-and-test.yml?branch=master&style=plastic
[12]:
  https://github.com/realazthat/mdremotifier/actions/workflows/build-and-test.yml
[13]:
  https://img.shields.io/github/commits-since/realazthat/mdremotifier/v0.5.0/master?style=plastic
[14]:
  https://github.com/realazthat/mdremotifier/compare/v0.5.0...master
[15]:
  https://img.shields.io/github/last-commit/realazthat/mdremotifier/master?style=plastic
[16]: https://github.com/realazthat/mdremotifier/tree/develop
[17]:
  https://img.shields.io/github/actions/workflow/status/realazthat/mdremotifier/build-and-test.yml?branch=develop&style=plastic
[18]:
  https://img.shields.io/github/commits-since/realazthat/mdremotifier/v0.5.0/develop?style=plastic
[19]:
  https://github.com/realazthat/mdremotifier/compare/v0.5.0...develop
[20]:
  https://img.shields.io/github/commits-since/realazthat/mdremotifier/v0.5.0/develop?style=plastic
[21]:
  https://github.com/realazthat/mdremotifier/compare/v0.5.0...develop
[22]:
  https://img.shields.io/github/last-commit/realazthat/mdremotifier/develop?style=plastic
[23]: https://github.com/realazthat/snipinator
[24]:
  https://github.com/realazthat/snipinator/blob/33c041210031bb1ef0ab9794f8fc56f3a9adb67b/README.md?plain=1
[25]:
  https://github.com/realazthat/snipinator/blob/33c041210031bb1ef0ab9794f8fc56f3a9adb67b/scripts/generate-readme.sh#L29
[26]:
  https://github.com/realazthat/snipinator/blob/33c041210031bb1ef0ab9794f8fc56f3a9adb67b/.github/README.remotified.md?plain=1
[27]: https://github.com/realazthat/excalidraw-brute-export-cli
[28]:
  https://github.com/realazthat/excalidraw-brute-export-cli/blob/8fa2ab033fb62fb0585b77d0966afe1a4b08d682/README.md?plain=1
[29]:
  https://github.com/realazthat/excalidraw-brute-export-cli/blob/8fa2ab033fb62fb0585b77d0966afe1a4b08d682/scripts/generate-readme.sh#L65
[30]:
  https://github.com/realazthat/excalidraw-brute-export-cli/blob/8fa2ab033fb62fb0585b77d0966afe1a4b08d682/.github/README.remotified.md?plain=1
[31]: https://ghcr.io/realazthat/mdremotifier
[32]:
  https://github.com/bdashore3/remark-github-images
  "Documentation is non-existent, but code looks very similar to mdremotifier"
[33]: https://github.com/laobie/WriteMarkdownLazily "Uploads to cloud."
[34]: https://github.com/crh19970307/mdul "Uploads to sm.ms"
[35]:
  https://github.com/SkyLee424/Go-MarkDown-Image-Transfer-Helper
  "Upload to Qiniu Cloud"
[36]: https://github.com/jen6/imgo "Upload to Google Drive"
[37]:
  https://github.com/chocoluffy/lazy-markdown
  "Uploads to LeanCloud, readme is a bit unclear"
[38]: https://github.com/loheagn/gopic "Upload to cloud, not clear which cloud"
[39]: https://github.com/Undertone0809/imarkdown "Doesn't yet have a CLI."
[40]:
  https://github.com/ravgeetdhillon/markdown-imgur-upload
  "Upload to imgur, a bit annoying because it requires you to put the images into a particular directory"
