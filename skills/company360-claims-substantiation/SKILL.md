---
name: company360-claims-substantiation
description: "Assess evidence applicability to specific pet product claims, variants, species, markets and study endpoints. Use for Company 360 or comparable Motif company deep dives requiring this research decision. Focus: Match product wording to relevant claim evidence."
metadata:
  source-skill: "motif-claims-substantiation-2026-11-23"
  source-version: "2026-11-23"
  source-sha256: "57fd06f0f2762caff365769d6ee23f5b837983442361a11f6d759a6919f5073e"
  source-bundle-sha256: "7ec68ea58abf20671df63ec5b784e3f90cfa32014b1c67ffc25754e4f696ac1f"
  display-name: "Motif Claims and veterinary substantiation"
  workbook-destination: "Claims register → claims evidence; validation register → validation entries"
---

# Claims and veterinary substantiation

## Deliverable and owning workbook

Claims register → claims evidence; validation register → validation entries. For a new company, confirm equivalent workbook and tab names with the planner.

## Method

1. Capture verbatim short label wording, product code, jurisdiction, use directions, effective edition and source. Locate primary study or product-specific accepted-claims entry.
2. Extract design, comparator, species, sample, application frequency, follow-up, endpoint, effect measure, funding, limitations and replication. Compare study formulation and dose with the marketed variant.
3. Grade substantiation as matched, partial, unverified or contradicted. Keep clinical endpoint, owner-reported outcomes, buying behavior and legal sign-off separate.
4. Return a claim matrix and exact missing study/label linkage required before making a proposed claim. Route professional or legal judgments to a qualified decision maker.

## Acceptance example

A US accepted-claims entry for one product code supports that named US label; it cannot establish a Canadian launch, comparative efficacy or repeat purchase.

## Evidence and handoff
Read the current assignment and latest founder scope. Use public desk research and sources already authorized for the project. Resolve evidence, entity, resource and observation IDs before a new search. Keep US and Canadian facts distinct. Reuse one canonical resource per publisher, edition and binary hash, with distinct observations per locator, entity, date and metric. Record inherited rows separately from newly checked or collected evidence. Use null for unavailable values and retain true zero only with a source that reports zero.

Stage additions with job ID, skill version, entity/brand, market, reporting window and basis, unit and currency, raw observation, value, evidence classification (fact/inference/assumption/unavailable), evidence ID, source edition/URL/exact locator, access date, coverage/denominator, limitation or competing evidence, proposed workbook/tab, and next action. When no source qualifies, include search terms, sources checked, access results and the decision affected. Reuse the same job key on retry. Keep separate assertions for conflicting values and identify both sources. Coordinate canonical workbook changes through the assigned publisher.

Emit an honest status receipt at handoff: queued, running, staged, in review, targeted rework, blocked or accepted; job ID, actual assignee, Eastern timestamp, evidence link, dependency, next action and blocker. Use the shared tracker when available. Count completion only against the agreed acceptance criterion.

## Claude notes

- Source: `motif-claims-substantiation-2026-11-23` (SKILL.md sha256 57fd06f0f276). The method text is the source's, word for word, except that the workbook line, the acceptance example and the project name are written generically (2 line(s)).
- No search recipes ship with this skill (no queries, engines or stop rules). Record search terms, sources checked and access results as the handoff section asks.
- Related skills in this set: company360-logic-challenge (independent review of claim assertions).
