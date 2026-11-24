---
name: company360-output-evaluation
description: "Evaluate a frozen workbook, deck or document against its assigned question and Motif production standards, and decide whether another pass helps. Use for Company 360 or comparable Motif company deep dives requiring this research decision. Focus: Judge objective fit and route targeted rework."
metadata:
  source-skill: "motif-output-evaluation-2026-11-23"
  source-version: "2026-11-23"
  source-sha256: "87f96100c1f04823a1de7cd3919f387ced111338edb539ad57e5df4f7c03592e"
  source-bundle-sha256: "7ec68ea58abf20671df63ec5b784e3f90cfa32014b1c67ffc25754e4f696ac1f"
  display-name: "Motif Output evaluation and rework"
  workbook-destination: "Decision scorecard → gate questions, amendments and QA; working-session record → release decision"
---

# Output evaluation and rework

## Deliverable and owning workbook

Decision scorecard → gate questions, amendments and QA; working-session record → release decision. For a new company, confirm equivalent workbook and tab names with the planner.

## Method

1. Read the original acceptance criteria, task packet and logic-challenge log. Record evaluator identity separately from the builder. Check all required work products, meaningful unknowns and source-to-claim links.
2. Run available Motif output-QA and grader standards on the actual exported file. For unavailable tooling, record which mechanical checks were run manually and which remain pending. Inspect editable native elements, formula integrity, labels, units, readability and footer/page numbers.
3. Issue accept, targeted rework or blocked by unavailable evidence. For rework name defect, owner, exact check and change likely to improve the outcome. Recheck only changed sections plus dependent exhibits.
4. Record release version, criteria met, open defects and evidence links. A passing design/format check cannot clear unsupported research claims.

## Acceptance example

A correct product-identifier exhibit fails an assignment asking how many packs sold. Return targeted rework when an unexamined source exists, otherwise identify the decisive missing measure.

## Evidence and handoff
Read the current assignment and latest founder scope. Use public desk research and sources already authorized for the project. Resolve evidence, entity, resource and observation IDs before a new search. Keep US and Canadian facts distinct. Reuse one canonical resource per publisher, edition and binary hash, with distinct observations per locator, entity, date and metric. Record inherited rows separately from newly checked or collected evidence. Use null for unavailable values and retain true zero only with a source that reports zero.

Stage additions with job ID, skill version, entity/brand, market, reporting window and basis, unit and currency, raw observation, value, evidence classification (fact/inference/assumption/unavailable), evidence ID, source edition/URL/exact locator, access date, coverage/denominator, limitation or competing evidence, proposed workbook/tab, and next action. When no source qualifies, include search terms, sources checked, access results and the decision affected. Reuse the same job key on retry. Keep separate assertions for conflicting values and identify both sources. Coordinate canonical workbook changes through the assigned publisher.

Emit an honest status receipt at handoff: queued, running, staged, in review, targeted rework, blocked or accepted; job ID, actual assignee, Eastern timestamp, evidence link, dependency, next action and blocker. Use the shared tracker when available. Count completion only against the agreed acceptance criterion.

## Required project document styling check before handoff

For every authored or updated project Word or native Google document, including daily PRD, TECH, learning and recap versions, match the Word Styling Template's title treatment: a visible #FF5B1F orange rule under the title (1 pt, 5 pt padding), or equivalent orange title shading. This project-specific accent is approved in addition to Motif's base palette. Preserve original publisher material. Render the final saved version to PDF. Run scripts/check_orange.py on the rendered PDF using PyMuPDF, NumPy and Pillow; retain the page and band-location result. Visually check placement and retain the existing footer, pagination, typography and content QA. A missing or misplaced accent, missing render, unverified final file or failed hard check blocks delivery. Correct the file and rerun before publishing or requesting recipient ingestion. A style definition or an orange text run alone does not pass.

## Visible update time
For every new or materially edited project deliverable, include one visible metadata line near the title (cover or workbook review tab): last updated : YYYY-MM-DD - hh:mm AM/PM ET. Set the actual America/New_York edit time and replace the previous timestamp in place. Retain dated observations, receipts and native revision history. Check the displayed value on the final render before handoff; a missing, stale or placeholder timestamp blocks release.

## Claude notes

- Source: `motif-output-evaluation-2026-11-23` (SKILL.md sha256 87f96100c1f0). The method text is the source's, word for word, except that the workbook line, the acceptance example and the project name are written generically (5 line(s)).
- No search recipes ship with this skill (no queries, engines or stop rules). Record search terms, sources checked and access results as the handoff section asks.
- Related skills in this set: company360-logic-challenge (challenge log this skill reads).
- Motif output-QA and grader standards map to the Claude skills motif-output-qa and motif-grader where they are installed.
- Orange title check: `pip install -r scripts/requirements.txt`, then `python scripts/check_orange.py <rendered.pdf>`. Exit code 1 blocks release. The script is unchanged; PyMuPDF prints a deprecation warning for `import fitz`, which does not affect the result.
