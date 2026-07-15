# Novelty Protocol — "New Identity" Candidate Chain

The engine's `underivable` channel (a pair that is numerically correct +
symbolic-exact proven + not derivable from the axioms) produces a
**candidate**; no automatic step can produce the CLAIM "a new identity was
found". The chain:

```
underivable pair (M16/M19: already exact-proven)
 └─ 1. Canonical presentation: the pair's smallest representative + LaTeX (serialize layer)
 └─ 2. Library comparison: structural matching against KNOWN_IDENTITIES
      (I1–I21+) — is it a re-parametrization of a known one? (the recovery
      table is the first filter here)
 └─ 3. Axiom-gap analysis: is the non-derivability NEW mathematics, or is it
      a known-but-not-encoded law of the axiom set? (if the latter, the
      output is classified as "missing axiom" not "new identity" — that too
      is valuable, but a different thing)
 └─ 4. Literature checklist (marking, not claim):
      □ Gil, Eur. Phys. J. Appl. Phys. 40, 1 (2007) — polarimetric algebra compilation
      □ Gil, J. Appl. Remote Sens. 8, 081599 (2014) — Mueller algebra review
      □ Cloude, Optik 75, 26 (1986) — covariance/spectral decomposition
      □ Ossikovski line (differential/depolarizing decompositions)
      □ Kuntman corpus (JOSA A 34,80; PRA 95,063819; PRB 98,045410;
        arXiv:1705.07147; AO 55,2543) — project PDFs
      □ General: Aiello-Woerdman linear algebra notes; Chipman
 └─ 5. EXPERT GATE: a candidate that passes 1-4 enters the report with the
      "no trace found in the literature" label; the physical-meaning/
      publication-worth ruling is WITH THE HUMAN (Kuntman/user —
      critical-decision threshold: external contact + physics interpretation).
```

## Negative-result discipline (M24)

An empty `underivable` channel is a reportable observation: "in the swept
fragment and size, the axiom set is empirically complete." This provides
evidence for extension prioritization (whichever fragment has saturated,
instead of deepening there, the language is extended).

## Record

Every sweep is persistent via the `reports/sweep-NN-results.json` artifact
(K21: config + seeds embedded, deterministic reproduction). If a candidate
emerges, this protocol's outputs of steps 1-4 go to the report, and the step-5
decision goes to the user.
