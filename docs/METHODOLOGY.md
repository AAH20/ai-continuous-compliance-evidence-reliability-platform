# Evidence and evaluation methodology

## Evidence levels

| Level | Meaning | External claim permitted |
|---|---|---|
| VERIFIED | Reproduced with retained, redacted artifacts | Yes, within tested scope |
| OBSERVED | Witnessed in an authorized environment | Descriptive only |
| DOCUMENTED | Supported by a dated primary source | Product capability only |
| SYNTHETIC_REFERENCE | Generated fixture used to test ControlSRE | Implementation proof only |
| UNVERIFIED | Marketing, unavailable, or unreproduced behavior | No numeric result |

## Qualification

Evidence is qualified only when all material gates pass. Gate results, input identifiers, evaluator version, evaluation time, and canonical receipt must be retained. A failed scope or temporal gate forces the dependent assertion to `unknown` or `not substantiated`; it cannot remain compliant.

## Population recall

The expected population must be derived independently from the evidence stream where practical. For example, AWS Organizations can define the account population while a different collector supplies per-account configuration evidence.

## Control SLOs

Required minutes represent the time during which the control must be both operating and provable. Valid minutes require qualified evidence. Missing evidence is not automatically a control failure, but it consumes assurance error budget because the state cannot be substantiated.

## Mapping

Mappings require source and target identifiers, relationship, strength, rationale, and source reference. `subset` and `intersect` relationships cannot propagate full compliance. Conflicting mappings are surfaced rather than averaged.

## AI evaluation

An agent must be tested for groundedness, citation support, authorization boundaries, prompt-injection resistance, deterministic tool behavior, abstention, and recovery. Agent-generated conclusions require human approval when they affect control status, audit representation, risk acceptance, customers, or Finance.

## Public results

A public result must include scope, audit period, dataset or artifact references, raw measurements, evaluator version, limitations, evidence level, and deterministic receipt. Named products receive no numeric ranking from documentation alone.
