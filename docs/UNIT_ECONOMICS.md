# Finance-safe unit economics

## Cost model

Operating cost includes collector execution, storage, orchestration, model inference, human review, and rework. Implementation cost remains separate so leaders can compare run-rate efficiency with total investment.

```text
cost per qualified evidence = operating cost / auditor-accepted evidence
```

Do not divide by collected files. Rejected, stale, incomplete, irrelevant, or period-invalid artifacts are not qualified outcomes.

## Verified benefit

```text
verified benefit = avoided labor + avoided audit rework
                 + expected-loss reduction
                 + Finance-approved attributable margin
```

Expected-loss reduction must preserve probability, magnitude, control-effectiveness assumptions, horizon, and model owner. It is not booked revenue.

## Commercial separation

| Measure | Meaning | Enters ROI |
|---|---|---:|
| Confirmed contract value exposed or unblocked | Value of an opportunity linked to an assurance dependency | No |
| Modeled pipeline influenced | Probability-weighted commercial scenario | No |
| Finance-approved attributable margin | Margin causally attributed under an approved method | Yes |

Attribution should use a pre-agreed baseline, decision timestamp, opportunity cohort, counterfactual or matched comparison where practical, and Finance approval. Never claim the full value of a contract was created by GRC automation merely because assurance was one dependency.

## Reference fixture

The included synthetic fixture yields:

- $3.84 operating cost per qualified evidence;
- $272,000 verified benefit before total cost;
- $195,600 net verified value;
- 2.5602 reference ROI;
- $420,000 confirmed contract value as context only;
- $210,000 modeled pipeline as context only; and
- $0 Finance-approved attributable margin.

These values validate the calculation boundary. They are not production claims.
