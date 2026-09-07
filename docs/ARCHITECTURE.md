# Architecture

ControlSRE is a reliability layer between operational telemetry and systems that consume assurance decisions.

## Components

1. **Inventory adapters** normalize expected AWS accounts, Kubernetes objects, workflow sources, and other authorized infrastructure records.
2. **Population reconciler** compares expected and observed identifiers before any control assertion is trusted.
3. **Evidence qualifier** applies provenance, integrity, scope, freshness, relevance, and temporal validity gates.
4. **Temporal control graph** links artifacts, infrastructure, controls, framework requirements, assessment periods, risks, and decisions.
5. **Control SLO engine** converts valid operating minutes into objectives, error budgets, burn rates, and incident states.
6. **Mapping engine** enforces explicit relationship semantics and blocks partial inheritance.
7. **Evolution engine** turns sanitized incidents and near misses into permanent regression cases.
8. **Economic boundary** separates confirmed commercial context, modeled influence, and Finance-approved attributable margin.
9. **Output adapters** produce OSCAL-aligned results, auditor evidence packs, board narratives, and customer-assurance packets.

## Trust boundaries

- External evidence is untrusted input.
- Collectors cannot approve their own evidence.
- LLM output is a proposed assertion until grounded and authorized.
- Successful workflow delivery is not evidence qualification.
- A GRC record is not automatically an operating control.
- Contract value cannot become ROI without Finance approval.

## Deployment profile

The reference implementation is stateless and dependency-free. A production deployment should add an append-only object store, a relational metadata store, a queue, secrets management, tenant isolation, signed receipts, observability, retention controls, and recovery testing.

The public web surface runs independently of the Python API and uses synthetic reference data. It does not accept or persist customer data.
