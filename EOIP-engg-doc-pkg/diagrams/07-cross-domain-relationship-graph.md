# 07-cross-domain-relationship-graph

```mermaid
flowchart LR
 J[Jira Story] --> MR[Merge Request]
 MR --> C[Commit]
 C --> F[Source File]
 F --> FN[Function]
 FN --> D[Dependency]
 D --> P[Pipeline/Build]
 P --> DOC[Documentation]
 J -. evidence .-> E[Provenance]
 FN -. evidence .-> E
 DOC -. evidence .-> E
```
