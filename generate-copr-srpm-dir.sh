#!/bin/bash

set -euo pipefail

name="$1"
resultdir="$2"
resultdir="$(realpath -- "$resultdir")"
specname="${3:-}"
if [[ -z ${specname} ]]; then
   specname="$name"
fi

pushd packages/"$name"

if [[ -d git-src ]]; then
    git submodule init ./git-src
fi

bash ../../makerpmpkg.sh -o srpm-outdir="$resultdir" srpm-outdir "$specname".spec
