# Checkout latency incident runbook

Use for alert `Checkout latency exceeds SLO` or incident INC0012042.

1. Confirm impact in the Commerce production overview dashboard.
2. Compare the alert start with the latest production deployment.
3. Inspect the `risk_decision_timeout` log aggregate; do not inspect customer payloads.
4. If retry fan-out is present, request the approved bounded-fallback change.
5. Verify p95 is below 450 ms for ten minutes and execute TC-901.
6. Attach the dashboard, deployment, change and test-run identifiers to the incident.

Rollback authority belongs to Commerce SRE. Emergency changes require an auditable ServiceNow approval.
