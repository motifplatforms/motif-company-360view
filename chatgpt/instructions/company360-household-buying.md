# Household buying and repeat (company360-household-buying)

Use this when: Estimate household purchase incidence, packs per buyer or repeat from comparable population and purchase evidence. Use for Company 360 or comparable Motif company deep dives requiring this research decision. Focus: Evaluate buyer incidence, purchase rate and repeat.

## Deliverable and owning workbook

Customer workbook → sizing denominators; sizing model → assumptions and annual reconciliation. For a new company, confirm equivalent workbook and tab names with the planner.

## Method

1. Define eligible household universe, country, species, lookback, product universe and shopping channels. Identify purchase occasion, unique buying household and panel weighting.
2. Compute incidence as buyers/eligible households and frequency as purchased packs/buying households within the same window. Define repeat cohort, observation horizon, eligibility and censoring.
3. Separate directly measured purchases from reported routines, feeding or intent. Track overlapping dog/cat households, suppressed cells and panel undercoverage.
4. Return raw numerator/denominator, weighting and source methodology, or specific gaps and their effect on modeled demand.

## Acceptance example

Ownership totals and daily-use percentages cannot supply purchase incidence for a specific product category.

## Evidence and handoff
Read the current assignment and latest founder scope. Use public desk research and sources already authorized for the project. Resolve evidence, entity, resource and observation IDs before a new search. Keep US and Canadian facts distinct. Reuse one canonical resource per publisher, edition and binary hash, with distinct observations per locator, entity, date and metric. Record inherited rows separately from newly checked or collected evidence. Use null for unavailable values and retain true zero only with a source that reports zero.

Stage additions with job ID, skill version, entity/brand, market, reporting window and basis, unit and currency, raw observation, value, evidence classification (fact/inference/assumption/unavailable), evidence ID, source edition/URL/exact locator, access date, coverage/denominator, limitation or competing evidence, proposed workbook/tab, and next action. When no source qualifies, include search terms, sources checked, access results and the decision affected. Reuse the same job key on retry. Keep separate assertions for conflicting values and identify both sources. Coordinate canonical workbook changes through the assigned publisher.

Emit an honest status receipt at handoff: queued, running, staged, in review, targeted rework, blocked or accepted; job ID, actual assignee, Eastern timestamp, evidence link, dependency, next action and blocker. Use the shared tracker when available. Count completion only against the agreed acceptance criterion.

## Notes

- No search recipes ship with this skill (no queries, engines or stop rules). Record search terms, sources checked and access results as the handoff section asks.
- Related skills in this set: company360-customer-routines (sends reported routines here for purchase-rate work).
