---
name: company360-product-pack-identity
description: "Identify a specific product, species, variant and the dated packaging hierarchy before any matched-price or unit comparison. Use for Company 360 or comparable Motif company deep dives requiring this research decision. Focus: Resolve exact products, retail packs and dated cases."
metadata:
  source-skill: "motif-product-pack-identity-2026-11-23"
  source-version: "2026-11-23"
  source-sha256: "9dbdd31215db5b37be9f83fbd37c14190d9079cb4e380cb9f650d1c546792ffd"
  source-bundle-sha256: "7ec68ea58abf20671df63ec5b784e3f90cfa32014b1c67ffc25754e4f696ac1f"
  display-name: "Motif Product and pack identity"
  workbook-destination: "Channel workbook → shelf observations; sizing model → player and SKU map"
---

# Product and pack identity

## Deliverable and owning workbook

Channel workbook → shelf observations; sizing model → player and SKU map. For a new company, confirm equivalent workbook and tab names with the planner.

## Method

1. Collect original product label and dated retailer/distributor record. Record country, language, flavor, species/weight band, net quantity, count, retail identifier and seller listing ID.
2. Assign identity as exact, partial, conflicting or unresolved. Require compatible variant and quantity, plus a shared verified identifier for cross-seller exact match. Flag recycled listings or multiple UPCs under one ASIN.
3. Separate consumer pack from trade case. Record catalog edition, retail UPC, case GTIN, packs per case and effective window. Leave unsupported dates and conversions blank.
4. Deliver a SKU crosswalk with both source locators and explicit mismatch reasons; route differences for review before unit values are calculated.

## Acceptance example

A retail UPC that a 2023 catalog lists at five packs per case and an April 2025 catalog lists at four keeps both dated values. A US original variant and a Canadian two-flavour variant of the same line remain separate products.

When two regional editions of one distributor catalog carry the same file date but list the same UPC and item at four packs per case in one region and five in the other, with different printed section revisions, record distributor region, file version, page and printed section revision independently of the actual effective date. Shipment configurations remain unknown.

## Evidence and handoff
Read the current assignment and latest founder scope. Use public desk research and sources already authorized for the project. Resolve evidence, entity, resource and observation IDs before a new search. Keep US and Canadian facts distinct. Reuse one canonical resource per publisher, edition and binary hash, with distinct observations per locator, entity, date and metric. Record inherited rows separately from newly checked or collected evidence. Use null for unavailable values and retain true zero only with a source that reports zero.

Stage additions with job ID, skill version, entity/brand, market, reporting window and basis, unit and currency, raw observation, value, evidence classification (fact/inference/assumption/unavailable), evidence ID, source edition/URL/exact locator, access date, coverage/denominator, limitation or competing evidence, proposed workbook/tab, and next action. When no source qualifies, include search terms, sources checked, access results and the decision affected. Reuse the same job key on retry. Keep separate assertions for conflicting values and identify both sources. Coordinate canonical workbook changes through the assigned publisher.

Emit an honest status receipt at handoff: queued, running, staged, in review, targeted rework, blocked or accepted; job ID, actual assignee, Eastern timestamp, evidence link, dependency, next action and blocker. Use the shared tracker when available. Count completion only against the agreed acceptance criterion.

## Claude notes

- Source: `motif-product-pack-identity-2026-11-23` (SKILL.md sha256 9dbdd31215db). The method text is the source's, word for word, except that the workbook line, the acceptance example and the project name are written generically (3 line(s)).
- No search recipes ship with this skill (no queries, engines or stop rules). Record search terms, sources checked and access results as the handoff section asks.
- Related skills in this set: company360-retail-offers (uses the SKU crosswalk); company360-unit-economics (needs pack identity); company360-market-sell-through (qualifies the product universe).
