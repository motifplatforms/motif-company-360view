---
name: company360-unit-economics
description: "Build auditable SKU × country × channel economics using dated inputs, competing scenarios and explicit unknowns. Use for Company 360 or comparable Motif company deep dives requiring this research decision. Focus: Reconcile cost drivers and local contribution ranges."
metadata:
  source-skill: "motif-unit-economics-2026-11-23"
  source-version: "2026-11-23"
  source-sha256: "5a903f3bbfaa6497fb32355768b56acdc99148ab504f3a2849b8bc3ba0f09e46"
  source-bundle-sha256: "7ec68ea58abf20671df63ec5b784e3f90cfa32014b1c67ffc25754e4f696ac1f"
  display-name: "Motif Unit economics and sensitivities"
  workbook-destination: "Sizing model → evidence inputs, assumptions and scenario tabs; evidence log → sources"
---

# Unit economics and sensitivities

## Deliverable and owning workbook

Sizing model → evidence inputs, assumptions and scenario tabs; evidence log → sources. For a new company, confirm equivalent workbook and tab names with the planner.

## Method

1. Resolve pack and offer identity and separate retail shelf, realized selling price, wholesale net revenue, discounts, refunds and taxes. Specify local currency and unit of account.
2. Bridge net revenue to landed product cost, channel fees, payment fees, freight, fulfillment, acquisition and repeat contribution. Record sign convention and gross/net basis; distinguish estimated inputs from sourced values.
3. Model plausible ranges only with disclosed assumptions and rationale. Calculate break-even and a key sensitivity, and verify units and signs independently. Keep cash/working-capital timings distinct from operating margin.
4. Return a reproducible calculation, assumption table, sensitivity and the inputs needed to narrow the result. Where revenue/cost scope is unknown, leave realized margin unavailable.

## Acceptance example

A dated shelf-price snapshot for a pack with a stated piece count supports a shelf price per piece; retailer margin, producer revenue and manufacturing cost remain unknown.

## Evidence and handoff
Read the current assignment and latest founder scope. Use public desk research and sources already authorized for the project. Resolve evidence, entity, resource and observation IDs before a new search. Keep US and Canadian facts distinct. Reuse one canonical resource per publisher, edition and binary hash, with distinct observations per locator, entity, date and metric. Record inherited rows separately from newly checked or collected evidence. Use null for unavailable values and retain true zero only with a source that reports zero.

Stage additions with job ID, skill version, entity/brand, market, reporting window and basis, unit and currency, raw observation, value, evidence classification (fact/inference/assumption/unavailable), evidence ID, source edition/URL/exact locator, access date, coverage/denominator, limitation or competing evidence, proposed workbook/tab, and next action. When no source qualifies, include search terms, sources checked, access results and the decision affected. Reuse the same job key on retry. Keep separate assertions for conflicting values and identify both sources. Coordinate canonical workbook changes through the assigned publisher.

Emit an honest status receipt at handoff: queued, running, staged, in review, targeted rework, blocked or accepted; job ID, actual assignee, Eastern timestamp, evidence link, dependency, next action and blocker. Use the shared tracker when available. Count completion only against the agreed acceptance criterion.

## Claude notes

- Source: `motif-unit-economics-2026-11-23` (SKILL.md sha256 5a903f3bbfaa). The method text is the source's, word for word, except that the workbook line, the acceptance example and the project name are written generically (2 line(s)).
- No search recipes ship with this skill (no queries, engines or stop rules). Record search terms, sources checked and access results as the handoff section asks.
- Related skills in this set: company360-product-pack-identity (pack identity); company360-retail-offers (offer identity and shelf price); company360-customer-routines (routine inputs).
