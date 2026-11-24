---
name: company360-retail-offers
description: "Compare dated retailer offers and track observed channel presence for one exact product, pack, seller, place and time. Use for Company 360 or comparable Motif company deep dives requiring this research decision. Focus: Capture matched shelf offers and channel availability."
metadata:
  source-skill: "motif-retail-offers-2026-11-23"
  source-version: "2026-11-23"
  source-sha256: "f3669b77ef3e3edf7e478dc4b2845046b065d3438dafe1d4f3d81f2d7fc24265"
  source-bundle-sha256: "7ec68ea58abf20671df63ec5b784e3f90cfa32014b1c67ffc25754e4f696ac1f"
  display-name: "Motif Retail offers and channel presence"
  workbook-destination: "Channel workbook → shelf observations and source ledger"
---

# Retail offers and channel presence

## Deliverable and owning workbook

Channel workbook → shelf observations and source ledger. For a new company, confirm equivalent workbook and tab names with the planner.

## Method

1. Use the identity crosswalk, common capture window and geography. Capture signed-out state, availability, seller versus platform, currency, quantity, timestamp and accessible locator.
2. Separate buy-once, first-order, promotion, cart-gated and recurring subscription offers. Log inaccessible offers and unknown prices.
3. Compute local-currency price per piece only from compatible quantities. For label-implied daily cost, cite the applicable species/weight-specific feeding rule. Preserve raw inputs and formula.
4. Return matched rows and a separate unresolved-offer list. Sales require qualifying transaction evidence.

## Acceptance example

A Canadian reseller policy supports terms, while a dated retailer card supports an offer. Neither reports actual packs purchased.

## Evidence and handoff
Read the current assignment and latest founder scope. Use public desk research and sources already authorized for the project. Resolve evidence, entity, resource and observation IDs before a new search. Keep US and Canadian facts distinct. Reuse one canonical resource per publisher, edition and binary hash, with distinct observations per locator, entity, date and metric. Record inherited rows separately from newly checked or collected evidence. Use null for unavailable values and retain true zero only with a source that reports zero.

Stage additions with job ID, skill version, entity/brand, market, reporting window and basis, unit and currency, raw observation, value, evidence classification (fact/inference/assumption/unavailable), evidence ID, source edition/URL/exact locator, access date, coverage/denominator, limitation or competing evidence, proposed workbook/tab, and next action. When no source qualifies, include search terms, sources checked, access results and the decision affected. Reuse the same job key on retry. Keep separate assertions for conflicting values and identify both sources. Coordinate canonical workbook changes through the assigned publisher.

Emit an honest status receipt at handoff: queued, running, staged, in review, targeted rework, blocked or accepted; job ID, actual assignee, Eastern timestamp, evidence link, dependency, next action and blocker. Use the shared tracker when available. Count completion only against the agreed acceptance criterion.

## Claude notes

- Source: `motif-retail-offers-2026-11-23` (SKILL.md sha256 f3669b77ef3e). The method text is the source's, word for word, except that the workbook line, the acceptance example and the project name are written generically (1 line(s)).
- No search recipes ship with this skill (no queries, engines or stop rules). Record search terms, sources checked and access results as the handoff section asks.
- Related skills in this set: company360-product-pack-identity (the identity crosswalk this skill starts from).
