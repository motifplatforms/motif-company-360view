---
name: company360-operating-capability
description: "Trace which operating entity owns, contracts or depends on a manufacturing, quality, distribution or fulfillment capability. Use for Company 360 or comparable Motif company deep dives requiring this research decision. Focus: Map supply, quality and fulfillment dependencies."
metadata:
  source-skill: "motif-operating-capability-2026-11-23"
  source-version: "2026-11-23"
  source-sha256: "8ea10b7575984d8466c0a6ba2d04dd6775e069dd7dfc7a0a56d0fb16ada1b377"
  source-bundle-sha256: "7ec68ea58abf20671df63ec5b784e3f90cfa32014b1c67ffc25754e4f696ac1f"
  display-name: "Motif Operating capability and fulfillment"
  workbook-destination: "Company register → coverage; evidence log → evidence and sources"
---

# Operating capability and fulfillment

## Deliverable and owning workbook

Company register → coverage; evidence log → evidence and sources. For a new company, confirm equivalent workbook and tab names with the planner.

## Method

1. Select a capability and entity-period; identify facility, location, disclosed operator, affected product family, dates, quality processes and route-to-market.
2. Source plant records, filings, public release or retailer fulfillment terms. Label capability as owned, contracted, inferred or unknown. Require explicit linkage to allocate a parent capability to a brand.
3. Record operating dependencies including lot/expiry handling, evidence of process transfer, inventory aging, pack and country differences. Distinguish capacity from utilization and sell-through.
4. Deliver a capability map and a build/acquire diligence gap list. Capture any missing private cost or facility information without outreach or supplier contact.

## Acceptance example

A group facility or distribution-point count does not establish throughput at a SKU or in Canada.

## Evidence and handoff
Read the current assignment and latest founder scope. Use public desk research and sources already authorized for the project. Resolve evidence, entity, resource and observation IDs before a new search. Keep US and Canadian facts distinct. Reuse one canonical resource per publisher, edition and binary hash, with distinct observations per locator, entity, date and metric. Record inherited rows separately from newly checked or collected evidence. Use null for unavailable values and retain true zero only with a source that reports zero.

Stage additions with job ID, skill version, entity/brand, market, reporting window and basis, unit and currency, raw observation, value, evidence classification (fact/inference/assumption/unavailable), evidence ID, source edition/URL/exact locator, access date, coverage/denominator, limitation or competing evidence, proposed workbook/tab, and next action. When no source qualifies, include search terms, sources checked, access results and the decision affected. Reuse the same job key on retry. Keep separate assertions for conflicting values and identify both sources. Coordinate canonical workbook changes through the assigned publisher.

Emit an honest status receipt at handoff: queued, running, staged, in review, targeted rework, blocked or accepted; job ID, actual assignee, Eastern timestamp, evidence link, dependency, next action and blocker. Use the shared tracker when available. Count completion only against the agreed acceptance criterion.

## Claude notes

- Source: `motif-operating-capability-2026-11-23` (SKILL.md sha256 8ea10b757598). The method text is the source's, word for word, except that the workbook line, the acceptance example and the project name are written generically (1 line(s)).
- No search recipes ship with this skill (no queries, engines or stop rules). Record search terms, sources checked and access results as the handoff section asks.
- Related skills in this set: company360-entity-portfolio (entity and period ownership).
