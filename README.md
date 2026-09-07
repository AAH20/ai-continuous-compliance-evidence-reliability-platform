# ControlSRE — AI Continuous Compliance & Evidence Reliability Platform

[![CI](https://github.com/AAH20/ai-continuous-compliance-evidence-reliability-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/AAH20/ai-continuous-compliance-evidence-reliability-platform/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Evidence](https://img.shields.io/badge/results-synthetic_reference-5ee7f2.svg)](docs/METHODOLOGY.md)

Open-source **continuous compliance**, **GRC automation**, **audit evidence collection**, **control monitoring**, **AI governance**, **cloud security compliance**, **Kubernetes compliance**, **cyber risk quantification**, and **revenue assurance**—engineered with SRE-style service-level objectives and error budgets.

ControlSRE answers the question that collection dashboards cannot answer alone:

> Is the evidence complete, current, period-valid, correctly mapped, reproducible, auditor-usable, and economically defensible?

The project complements GRC platforms, workflow tools, cloud-native assessment services, SIEMs, and observability stacks. It does not claim to replace them.

## Why control reliability engineering

A successful connector run does not prove that every required account, cluster, region, asset, page, control, or audit period was covered. A green result from incomplete input is more dangerous than an explicit failure.

ControlSRE establishes:

- an expected-versus-observed population reconciler;
- a six-gate evidence qualification pipeline;
- bitemporal audit and evidence semantics;
- control SLOs, error budgets, burn rates, and reliability incidents;
- conservative framework cross-mapping;
- deterministic receipts and replay;
- a regression evolution loop for production near misses; and
- Finance-controlled revenue-assurance economics.

## Evidence decision path

```text
AWS · Kubernetes · CI/CD · IAM · ticketing · SIEM · GRC APIs
                              ↓
                   Expected population graph
                              ↓
                     Immutable evidence receipt
                              ↓
     Provenance · Integrity · Scope · Freshness · Relevance · Time
                              ↓
                   Temporal control knowledge graph
                              ↓
           Control SLO · error budget · drift · incident state
                              ↓
       OSCAL result · auditor pack · board pack · customer assurance
                              ↓
             Finance-approved attributable commercial value
```

## Current release

- Python package and `controlsre` CLI
- Dependency-free local HTTP API
- AWS Organizations, Kubernetes, and workflow inventory normalization contracts
- Expected-versus-observed population reconciliation
- Evidence provenance, integrity, scope, freshness, relevance, and temporal gates
- Control availability, error-budget, and burn-rate calculations
- Fail-closed framework relationship semantics
- Mapping-conflict detection
- CISO Assistant-compatible framework catalog import
- Incident-to-regression sanitization
- Finance-safe unit economics
- Deterministic SHA-256 receipts
- 18 synthetic failure scenarios
- Importable n8n reference workflow
- Zapier integration blueprint
- GitHub Action and CI release gate
- Interactive assurance command surface

All included operational and economic values are synthetic references. They prove the implementation and contracts—not production performance, customer outcomes, or vendor rankings.

## Control SLOs

```text
control availability
= valid compliant minutes / required operating minutes

allowed bad minutes
= required minutes × (1 − objective)

burn rate
= observed bad-minute rate / allowed bad-minute rate
```

The reference `LOG-02` case evaluates a 90-day requirement with a 99.5% objective. The included fixture produces 98.72% availability, exhausts its error budget, and enters `burning` state.

## Six evidence gates

| Gate | Required proof | Fail-closed condition |
|---|---|---|
| Provenance | Source, resource, collector | Origin cannot be established |
| Integrity | Canonical payload digest | Retained receipt does not match |
| Scope | Expected population is observed | Account, cluster, region, asset, or page is missing |
| Freshness | Artifact meets its age SLO | Collection is stale or from the future |
| Relevance | Artifact supports evaluated controls | Target objective is not substantiated |
| Temporal validity | Collection and evaluation fit validity and audit windows | Evidence cannot prove the required period |

Material failures cannot be averaged away by unrelated passing checks.

## Framework cross-mapping

Supported relationship semantics:

- `equal`
- `superset`
- `subset`
- `intersect`
- `conflicts_with`
- `requires_additional_evidence`

Only qualified assertions connected through `equal` or `superset` relationships can inherit a compliant result. Partial or conflicting relationships require target-specific evidence.

The import contract can integrate with the 150+ framework surface available in CISO Assistant. This repository includes four structural fixtures only; it does not copy, relicense, or claim ownership of upstream framework content.

## Failure laboratory

The 18-case reference catalog covers:

| Category | Examples |
|---|---|
| Population | Omitted AWS account, omitted Kubernetes cluster, partial pagination |
| Authorization | Expired token, silent permission loss |
| Time | Stale artifact, audit-period mismatch |
| Integrity | Payload digest modification |
| Mapping | Partial mapping promoted to full, conflicting relationships |
| Delivery | Schema drift, duplicate webhook, out-of-order observation |
| Agent safety | Prompt injection, unsupported assertion, unauthorized approval |
| Finance | Full contract value inserted into ROI |
| Reproducibility | Identical inputs generate inconsistent outcomes |

See [`fixtures/failure-scenarios.json`](fixtures/failure-scenarios.json).

## KPI release gates

| KPI | Initial target |
|---|---:|
| Evidence population recall | ≥99% |
| Evidence qualification precision | ≥98% |
| Provenance completeness | 100% |
| False-compliant escape rate | ≤0.1% |
| Stale-evidence escape rate | ≤0.5% |
| Deterministic replay agreement | ≥99.9% |
| Critical mapping-conflict detection | 100% |
| Collector availability | ≥99.5% |
| Evidence-pipeline failure detection | <5 minutes |
| Recoverable connector failure success | ≥95% |
| Auditor first-pass evidence acceptance | ≥90% |

Targets are evaluation gates. They are not claims about an untested deployment.

## Finance-safe unit economics

```text
cost per qualified evidence
= (collection + storage + orchestration + model + review + rework)
  / auditor-accepted artifacts

net verified value
= avoided labor + avoided audit rework + expected-loss reduction
  + Finance-approved attributable margin
  − implementation and operating cost
```

ControlSRE always separates:

1. confirmed contract value exposed or unblocked;
2. modeled or influenced pipeline; and
3. Finance-approved attributable margin.

Only the third commercial measure enters verified benefit and ROI. See [`docs/UNIT_ECONOMICS.md`](docs/UNIT_ECONOMICS.md).

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v

controlsre qualify fixtures/evidence-valid.json \
  --as-of 2026-09-07T12:00:00Z

controlsre coverage fixtures/population.json
controlsre slo fixtures/control-slo.json
controlsre economics fixtures/economics.json
controlsre serve --host 127.0.0.1 --port 8788
```

Run the decision surface:

```bash
npm install
npm run dev
```

## Integration surface

- AWS Organizations, Config, CloudTrail, IAM, and Security Hub
- Kubernetes audit events, admission policy, and workload inventory
- CI/CD and infrastructure-as-code change records
- Elastic, OpenSearch, VictoriaLogs, and Wazuh-derived signals
- n8n and Zapier execution records
- ticket, policy, audit-request, and customer-assurance workflows
- OSCAL assessment results and POA&M flows
- CISO Assistant-compatible framework catalogs
- authorized proprietary GRC APIs

The reference adapters normalize synthetic records. Production connectors require authorized credentials, tenant-specific scoping, rate-limit handling, secret management, and independent verification.

## Evolution loop

```text
incident or near miss → sanitized fixture → deterministic and agentic regression
→ shadow replay → GRC/control-owner approval → progressive release → SLO watch
```

Sensitive incident data is rejected from the regression-case builder. Every accepted case receives a deterministic receipt.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Evidence and evaluation methodology](docs/METHODOLOGY.md)
- [Unit economics](docs/UNIT_ECONOMICS.md)
- [Platform boundaries and alternatives](docs/PLATFORM_BOUNDARIES.md)
- [Security policy](SECURITY.md)
- [OpenAPI contract](contracts/controlsre.openapi.yaml)

## Responsible use

- Use only authorized accounts, tenants, APIs, and infrastructure.
- Never scrape private tenants, bypass access controls, or copy licensed framework text.
- Treat collected documents and external records as untrusted data.
- Require human approval for compliance conclusions, risk acceptance, external communication, and revenue attribution.
- Retain redacted artifacts sufficient for independent reproduction.

## License

Apache-2.0. Framework texts, vendor documentation, trademarks, and customer data remain the property of their respective owners.
