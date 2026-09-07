# Zapier integration contract

Use **Webhooks by Zapier** to POST an evidence record to `/v1/evidence/qualify` and branch only on the returned `qualified` field. A successful HTTP transport is not a compliance decision.

Required safeguards:

- store the ControlSRE base URL and authentication outside the Zap definition;
- retain the returned receipt hash;
- route every failed gate to a human-owned incident;
- use an idempotency key derived from the source artifact ID and collector version;
- never let a Zap approve a control, accept risk, or attribute revenue.
