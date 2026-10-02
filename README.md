# AAT Scheme Performance Engine

Portrait-tablet Streamlit surface for **predictive operational risk & long-tail claims governance** (NZD).

## Views

| View | Purpose |
| --- | --- |
| **Global Scheme Portfolio** | 3-column metrics, slim ledger (`Claim ID` / `Anatomy Target` / `Status`), CapEx velocity |
| **Log New Claimant Profile** | Unlocked triage → live Comprehensive Scheme Ledger Dossier |
| **Individual claim drill-down** | Consolidated dossier card (metadata + NLP + PPD/TASE/reserve) + alignment vector + time-cost axis |

## Dossier

- Critical → crimson PPD · Nominal → green PPD  
- CapEx floor drives Mitigated Capital Reserve Target  
- Lookback valuation Director-only (others see executive proxy)  

## Evidentiary and statutory gates

The docket workflow requires three timezone-qualified, strictly ordered telemetry
observations with changing values and at least one deviation beyond the configured
noise band before sealing telemetry. The payload is SHA-256 checked against its
session-local anchor before statutory clearance.

Before a dossier can advance from legal review to the executive vault, the demo
requires a separate assessor identity, a non-matching executive email, an
independence attestation, evidence-integrity sign-off, and statutory clearance.
The decision deadline is set by the app and checked again at execution. Failed
checks report `ERR_GOV_CONFLICT_OF_INTEREST`, `ERR_EVID_INTEGRITY_TAMPERED`,
`ERR_MATH_NO_OBSERVED_DRIFT`, `ERR_TIME_DEADLINE_LAPSED`, or
`ERR_STATUTORY_GATE_BLOCKED`.

These are workflow controls for the demo, not production identity or evidence
services. Assessor details and attestations are not authenticated, and evidence
hashing covers the in-session telemetry snapshot only; external repository files,
durable immutable storage, and legal compliance must be verified by production
services and qualified reviewers.
