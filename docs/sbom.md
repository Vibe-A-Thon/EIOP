# Software Bill of Materials (SBOM)

**Status:** implemented (CC3-017 closure, per `EOIP-engg-doc-pkg/69-dependency-license-sbom.md`)

## Generation

```bash
.venv/Scripts/python scripts/generate_sbom.py --output sbom.cyclonedx.json --validate
```

The generator is stdlib-only and fully offline. It emits a single merged
CycloneDX 1.5 JSON document covering three ecosystems:

| Ecosystem | Source | CycloneDX type |
|---|---|---|
| Python | `importlib.metadata` of the running interpreter (the release venv; `pip freeze` equivalent) | `library`, purl `pkg:pypi/...` |
| npm | `apps/web/package-lock.json` (lockfileVersion 3 `packages` map, includes transitive deps) | `library`, purl `pkg:npm/...` |
| container | `image:` lines in `deploy/docker-compose*.yml` and `FROM` lines in `deploy/Containerfile`/`Dockerfile` | `container`, purl `pkg:docker/...` |

Every component carries an `eoip:ecosystem` property. Container components also
carry `eoip:referenced_by` (which compose/Dockerfile references them) and
`eoip:digest_pinned` (`false` for tag-only references — see limitations).

## License classification

Licenses are resolved in priority order:

1. **`licenses/` evidence directory** — package-pinned license texts named
   `<package>-<version>[-LICENSE|COPYING].(txt|md)` (e.g. `numpy-2.4.6-LICENSE.txt`).
   The SPDX identifier is detected from the text and the component gets an
   `eoip:license_evidence` property pointing at the file.
2. **Package-declared metadata** — `License-Expression`, `License`, or
   `License :: OSI Approved ::` classifiers from Python dist metadata.
3. **`NOASSERTION`** when neither source determines a license.

Known gap: the npm lockfile does not carry license fields, so npm components
without a `licenses/` entry are `NOASSERTION`. Reconciling these against
`node_modules/**/package.json` (or an npm audit feed) is follow-up work; the
83 npm components at the time of writing are listed in the generated SBOM with
`NOASSERTION` so the gap is explicit rather than silent.

## Validation

`--validate` runs structural validation of the generated document and exits
non-zero on any problem:

- `bomFormat`/`specVersion`/`serialNumber`/`metadata` required fields;
- `components` is a non-empty list; each component has `type`, `bom-ref`,
  `name`, `version`, `purl`;
- `bom-ref` uniqueness across the merged ecosystems;
- purl shape (`pkg:pypi|npm|docker|oci/...@...`).

Validation against the official CycloneDX JSON schema requires the schema file
(`cyclonedx/schema/bom-1.5.schema.json`) or the `cyclonedx-bom` CLI, which are
not vendored; `--validate` is the offline gate. The most recent run:

```
SBOM written to sbom.cyclonedx.json (110597 bytes)
components: container=15, npm=83, pypi=142
structural validation: OK
```

## Remaining CC3-017 scope not closed here

- Image digest pinning (`@sha256:`) for release compose files — components are
  flagged with `eoip:digest_pinned=false` until done.
- Image vulnerability scanning and the offline/air-gap install validation run.
