# Documentum Connector API Research & Qualification Specification

*Researched per CRA-006.3, CRA-006.7. Complies with ADR-004, ONT-006.*

## Official API Specifications & Pinned Versions
- **Documentum REST Services & CMIS 1.1**:
  - Pinned API endpoint: `/dctm-rest/repositories/{repository}`
  - Resources: `/cabinets`, `/cabinets/{id}/sysobjects`, `/folders/{id}/sysobjects`
  - CMIS AtomPub / Browser bindings for enterprise content management.

## Document Identity & Version Lineage
- **Core Principle**: Document identity is NEVER reduced to a file name or web URL.
- **Persistent Identifiers**:
  - Object ID: `r_object_id` (16-character hexadecimal unique identifier).
  - Version Chronicle: `i_chronicle_id` anchors the entire version history across branches and checkouts.
  - Version Label: `r_version_label` (e.g., `1.0`, `1.1`, `CURRENT`).

## Cabinets, Folders, and Renditions
- Cabinet and Folder hierarchy preserved with `locatedIn` relationship.
- Renditions: primary format and converted renditions (e.g. PDF, thumbnail) tracked with size and format attributes.

## Governance, Retention, and Legal Hold
- Documentum ACLs: `acl_name` and `acl_domain` mapped into `PermissionMetadata.principal_refs`.
- Retention Policy: `r_retention_until` date preserved.
- Legal Hold: `r_immutable_flag` and hold locks strictly reflected in metadata and access rules.
