#!/bin/bash
set -eEuo pipefail
HERE="$(cd "$(dirname "$0")"; pwd)"

if ! [[ -x jekyll ]]; then
  cat >&2 <<EOF
Jekyll not found.
To install:
  sudo apt-get install ruby-full build-essential zlib1g-dev
  gem install jekyll bundler
EOF
  exit 1
fi

set -x
cd "$HERE"
jekyll build
jekyll serve
