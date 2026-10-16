# 14-web-ui-architecture

```mermaid
graph LR
 Browser[React SPA] --> Search[Search/Query]
 Browser --> Graph[Graph Explorer]
 Browser --> Impact[Trace/Impact]
 Browser --> Admin[Admin Screens]
 Search --> API[FastAPI]
 Graph --> API
 Impact --> API
 Admin --> API
 API --> Services[Application Services]
```
