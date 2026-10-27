#!/usr/bin/env bash
# Fetch the W3C SPARQL test suite (w3c/rdf-tests) at a pinned commit (CRA-024.7).
# The commit id is the integrity check: git verifies every object against it, so the manifests,
# queries, data and expected results are exactly those of the pinned revision.
set -euo pipefail
RDF_TESTS_COMMIT="${RDF_TESTS_COMMIT:-bfefa770267ec0e5b6e45764bbca4ee43789ba72}"
DEST="${1:-.cache/rdf-tests}"
if [ ! -d "$DEST/.git" ]; then
  git init -q "$DEST"
  git -C "$DEST" remote add origin https://github.com/w3c/rdf-tests.git
fi
git -C "$DEST" fetch -q --depth 1 origin "$RDF_TESTS_COMMIT"
git -C "$DEST" -c advice.detachedHead=false checkout -q FETCH_HEAD
test "$(git -C "$DEST" rev-parse HEAD)" = "$RDF_TESTS_COMMIT"
echo "w3c/rdf-tests @ $RDF_TESTS_COMMIT -> $DEST/sparql/sparql11"
