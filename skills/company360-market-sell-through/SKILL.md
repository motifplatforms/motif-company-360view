---
name: company360-market-sell-through
description: "Measure and reconcile annual or matched 52-week retail sell-through, market scope, currency and covered outlets. Use for Company 360 or comparable Motif company deep dives requiring this research decision. Focus: Measure comparable sales, units and market coverage."
metadata:
  source-skill: "motif-market-sell-through-2026-11-23"
  source-version: "2026-11-23"
  source-sha256: "541347d3e4e77b4dfed58d7d803824875f22a9cac661bd53f74fc27d86eb3a76"
  source-bundle-sha256: "7ec68ea58abf20671df63ec5b784e3f90cfa32014b1c67ffc25754e4f696ac1f"
  display-name: "Motif Market measurement and sell-through"
  workbook-destination: "Sizing model → market measurement tabs; evidence log → sizing source intake"
---

# Market measurement and sell-through

## Deliverable and owning workbook

Sizing model → market measurement tabs; evidence log → sizing source intake. For a new company, confirm equivalent workbook and tab names with the planner.

## Method

1. Freeze eligible product and channel universe; state geography, periods, local currency, reporting basis, and included outlets. Align a 52-week comparison before labeling US/Canada rows comparable.
2. Look for public reports and POS disclosures with measured packs and consumer dollars. Record manufacturer shipments, weighted panel projections and parent totals with their distinct scope.
3. Validate money/pack/piece/net-weight reconciliation; retain local units and dated pack factors. Split 2020–25 annual observations, 2026 YTD, 2026 estimate, and 2027–31 forecast.
4. Return category/line/SKU facts, missing numerator or denominator, and a sensitivity or coverage bridge for each decision. A documented search can yield unavailable.

## Acceptance example

A blank sell-through cell remains missing. Reject automatic allocation of a parent's segment growth or category revenue to a single SKU.

## Evidence and handoff
Read the current assignment and latest founder scope. Use public desk research and sources already authorized for the project. Resolve evidence, entity, resource and observation IDs before a new search. Keep US and Canadian facts distinct. Reuse one canonical resource per publisher, edition and binary hash, with distinct observations per locator, entity, date and metric. Record inherited rows separately from newly checked or collected evidence. Use null for unavailable values and retain true zero only with a source that reports zero.

Stage additions with job ID, skill version, entity/brand, market, reporting window and basis, unit and currency, raw observation, value, evidence classification (fact/inference/assumption/unavailable), evidence ID, source edition/URL/exact locator, access date, coverage/denominator, limitation or competing evidence, proposed workbook/tab, and next action. When no source qualifies, include search terms, sources checked, access results and the decision affected. Reuse the same job key on retry. Keep separate assertions for conflicting values and identify both sources. Coordinate canonical workbook changes through the assigned publisher.

Emit an honest status receipt at handoff: queued, running, staged, in review, targeted rework, blocked or accepted; job ID, actual assignee, Eastern timestamp, evidence link, dependency, next action and blocker. Use the shared tracker when available. Count completion only against the agreed acceptance criterion.

## Claude notes

- Source: `motif-market-sell-through-2026-11-23` (SKILL.md sha256 541347d3e4e7). The method text is the source's, word for word, except that the workbook line, the acceptance example and the project name are written generically (2 line(s)).
- No search recipes ship with this skill (no queries, engines or stop rules). Record search terms, sources checked and access results as the handoff section asks.
- Related skills in this set: company360-product-pack-identity (signed-off SKU list); company360-household-buying (purchase denominators).
