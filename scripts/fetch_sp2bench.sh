#!/usr/bin/env bash
# Fetch SP2Bench (Schmidt et al., ICDE 2009; BSD) queries Q1-Q12c and documents produced by the official
# SP2Bench data generator, as published in RDFLib/rdflib-benchmark at a pinned commit (CRA-024 A.2).
# Only the needed blobs are downloaded; git verifies each against the pinned commit, and the sha256 of every
# file used is checked against scripts/sp2bench.sha256 as a second, tool-independent check.
set -euo pipefail
SP2B_COMMIT="${SP2B_COMMIT:-456f7b1c3e9dbcf099b8267155970b5156c4e253}"
DEST="${1:-.cache/sp2bench}"
SIZES="${SP2B_SIZES:-16000 1024000}"
here="$(cd "$(dirname "$0")" && pwd)"
if [ ! -d "$DEST/.git" ]; then
  git init -q "$DEST"
  git -C "$DEST" remote add origin https://github.com/RDFLib/rdflib-benchmark.git
fi
git -C "$DEST" sparse-checkout set --no-cone /sp2b/queries/ $(for s in $SIZES; do printf '/sp2b/%s.n3.bz2 ' "$s"; done)
git -C "$DEST" fetch -q --depth 1 --filter=blob:none origin "$SP2B_COMMIT"
git -C "$DEST" -c advice.detachedHead=false checkout -q FETCH_HEAD
test "$(git -C "$DEST" rev-parse HEAD)" = "$SP2B_COMMIT"
(cd "$DEST" && grep -E "sp2b/queries/|$(echo $SIZES | sed 's/ /|/g')" "$here/sp2bench.sha256" | sha256sum -c --quiet -)
echo "SP2Bench @ $SP2B_COMMIT -> $DEST/sp2b (sizes: $SIZES)"
