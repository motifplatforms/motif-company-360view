---
name: company360-entity-portfolio
description: "Determine which operating, brand, line or licensed entity owned an asset during a stated period. Use for Company 360 or comparable Motif company deep dives requiring this research decision. Focus: Trace company ownership and portfolio changes."
metadata:
  source-skill: "motif-entity-portfolio-2026-11-23"
  source-version: "2026-11-23"
  source-sha256: "336333ec81c669788e413c0dbcded30d17e9809481c4b1f0698cc8081986cb97"
  source-bundle-sha256: "7ec68ea58abf20671df63ec5b784e3f90cfa32014b1c67ffc25754e4f696ac1f"
  display-name: "Motif Entity and portfolio"
  workbook-destination: "Company register → entities and coverage; evidence log → sources"
---

# Entity and portfolio

## Deliverable and owning workbook

Company register → entities and coverage; evidence log → sources. For a new company, confirm equivalent workbook and tab names with the planner.

## Method

1. Resolve the supplied alias to a stable entity ID and assign the parent assignment only once across sibling brands. Record beneficial owner, operating company and trademark/license relationships as distinct roles.
2. Read issuer disclosures, filings and transaction closing notices; capture announcement and close dates separately. Preserve indeterminate start/end dates.
3. Reconcile company, segment, brand and product-line scope before linking an annual figure. Distinguish consolidation from retail selling activity.
4. Return a dated edge list (child, parent, role, valid_from/to, scope) and a parent exhibit that sibling chapters can reference.

## Acceptance example

Two brands owned by the same parent require one parent dossier; growth the issuer reports for a different product line stays scoped to that line.

## Evidence and handoff
Read the current assignment and latest founder scope. Use public desk research and sources already authorized for the project. Resolve evidence, entity, resource and observation IDs before a new search. Keep US and Canadian facts distinct. Reuse one canonical resource per publisher, edition and binary hash, with distinct observations per locator, entity, date and metric. Record inherited rows separately from newly checked or collected evidence. Use null for unavailable values and retain true zero only with a source that reports zero.

Stage additions with job ID, skill version, entity/brand, market, reporting window and basis, unit and currency, raw observation, value, evidence classification (fact/inference/assumption/unavailable), evidence ID, source edition/URL/exact locator, access date, coverage/denominator, limitation or competing evidence, proposed workbook/tab, and next action. When no source qualifies, include search terms, sources checked, access results and the decision affected. Reuse the same job key on retry. Keep separate assertions for conflicting values and identify both sources. Coordinate canonical workbook changes through the assigned publisher.

Emit an honest status receipt at handoff: queued, running, staged, in review, targeted rework, blocked or accepted; job ID, actual assignee, Eastern timestamp, evidence link, dependency, next action and blocker. Use the shared tracker when available. Count completion only against the agreed acceptance criterion.

## Claude notes

- Source: `motif-entity-portfolio-2026-11-23` (SKILL.md sha256 336333ec81c6). The method text is the source's, word for word, except that the workbook line, the acceptance example and the project name are written generically (2 line(s)).
- No search recipes ship with this skill (no queries, engines or stop rules). Record search terms, sources checked and access results as the handoff section asks.
- Related skills in this set: company360-decision-synthesis (uses the parent exhibit); company360-operating-capability (needs the entity-period).
