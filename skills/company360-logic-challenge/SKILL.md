---
name: company360-logic-challenge
description: "Independently challenge completed research assertions, fiscal periods, market scopes, source independence, denominators, calculations and competing explanations. Use for Company 360 or comparable Motif company deep dives requiring this research decision. Focus: Adjudicate material claims and counter-evidence."
metadata:
  source-skill: "motif-logic-challenge-2026-11-23"
  source-version: "2026-11-23"
  source-sha256: "80f24e51f11d1968c8439d5de408a01a57eee1e8c728a74cace111aed0d091b7"
  source-bundle-sha256: "7ec68ea58abf20671df63ec5b784e3f90cfa32014b1c67ffc25754e4f696ac1f"
  display-name: "Motif Independent research logic challenge"
  workbook-destination: "Validation register → validation entries, scoped calculations and daily resolution log"
---

# Independent research logic challenge

## Deliverable and owning workbook

Validation register → validation entries, scoped calculations and daily resolution log. For a new company, confirm equivalent workbook and tab names with the planner.

## Method

1. Obtain the frozen assertion and raw evidence bundle. Reviewer must be separate from the assertion builder; record reviewer identity and actual independence. In its absence mark awaiting independent review.
2. Open the original publication and exact locator; recompute any measure from raw facts and units. Test alternate interpretations, publication reuse, denominators, attribution and currency/period compatibility.
3. Create challenge IDs linked to assertion and source IDs. Propose a precise fix; return supported, qualified or withheld per assertion. A separate author remediates defects and reviewer rechecks the changed assertion.
4. Return an immutable challenge log with disposition, reasoning, references, severity, changed cells and reopen conditions. Source access failures remain visible.

## Acceptance example

References to the same third-party market report count as one publication; assigning its table headings numerical sales values fails the challenge.

## Evidence and handoff
Read the current assignment and latest founder scope. Use public desk research and sources already authorized for the project. Resolve evidence, entity, resource and observation IDs before a new search. Keep US and Canadian facts distinct. Reuse one canonical resource per publisher, edition and binary hash, with distinct observations per locator, entity, date and metric. Record inherited rows separately from newly checked or collected evidence. Use null for unavailable values and retain true zero only with a source that reports zero.

Stage additions with job ID, skill version, entity/brand, market, reporting window and basis, unit and currency, raw observation, value, evidence classification (fact/inference/assumption/unavailable), evidence ID, source edition/URL/exact locator, access date, coverage/denominator, limitation or competing evidence, proposed workbook/tab, and next action. When no source qualifies, include search terms, sources checked, access results and the decision affected. Reuse the same job key on retry. Keep separate assertions for conflicting values and identify both sources. Coordinate canonical workbook changes through the assigned publisher.

Emit an honest status receipt at handoff: queued, running, staged, in review, targeted rework, blocked or accepted; job ID, actual assignee, Eastern timestamp, evidence link, dependency, next action and blocker. Use the shared tracker when available. Count completion only against the agreed acceptance criterion.

## Claude notes

- Source: `motif-logic-challenge-2026-11-23` (SKILL.md sha256 80f24e51f11d). The method text is the source's, word for word, except that the workbook line, the acceptance example and the project name are written generically (2 line(s)).
- No search recipes ship with this skill (no queries, engines or stop rules). Record search terms, sources checked and access results as the handoff section asks.
- Related skills in this set: company360-output-evaluation (next stage after challenge).
