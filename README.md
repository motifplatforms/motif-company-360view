# motif-company-360view

Motif Platforms' 15 Claude skills for conducting 360 research on companies. Together they cover the desk research behind a full view of a company: entity and portfolio, product and pack identity, retail offers, sell-through, household buying, customer routines, positioning, claims, operating capability, unit economics, logic challenge, output evaluation, synthesis, work planning and the weekly tools review. A Claude session can pick up the same work with the same evidence rules.

Each skill sets out a method, an acceptance example and the evidence rules for handing work on. The examples are generic: they name no brand, product, catalog or private workbook, and each keeps the rule it teaches. A daily check keeps the skills in step with Motif's latest research methods.

## Install

As a Claude Code plugin (this repo is also its own marketplace):

```
/plugin marketplace add motifplatforms/motif-company-360view
/plugin install motif-company-360view@motif-company-360view
```

Or copy the folders under `skills/` into a project's `.claude/skills/`. Skills load by their description; in Claude Code you can also call one directly, for example `/motif-company-360view:company360-retail-offers`.

The output-evaluation skill runs a Python check on rendered PDFs:

```
pip install -r skills/company360-output-evaluation/scripts/requirements.txt
python skills/company360-output-evaluation/scripts/check_orange.py <rendered.pdf>
```

## Skills

| Skill | Job |
|---|---|
| company360-entity-portfolio | Which entity owned a brand, line or license in a stated period |
| company360-product-pack-identity | Exact product, variant and dated pack/case hierarchy |
| company360-retail-offers | Dated retailer offers and channel presence for one exact pack |
| company360-market-sell-through | Comparable sell-through, units and market coverage |
| company360-household-buying | Buyer incidence, purchase rate and repeat |
| company360-customer-routines | Coded customer routines, switching and unmet needs |
| company360-positioning-journey | Brand promises and purchase journey by channel |
| company360-claims-substantiation | Product claim wording against study evidence |
| company360-operating-capability | Manufacturing, quality and fulfillment dependencies |
| company360-unit-economics | SKU by country by channel economics and sensitivities |
| company360-decision-synthesis | Reviewed evidence into a founder decision exhibit |
| company360-work-planning | Job IDs, dependencies, owners and controlled publication |
| company360-logic-challenge | Independent challenge of finished assertions |
| company360-output-evaluation | Fit-to-question check, Motif QA and the orange title gate |
| company360-weekly-tools-review | Weekly adopt, defer or reject of tool changes |

## Known gaps

- No search recipes: the skills ask for search terms to be recorded but ship no queries, engines or stop rules. None were invented here.
- Each skill names the kind of workbook it writes to (company register, evidence log, channel workbook, sizing model and so on). Map these to your own files; each skill says to confirm the names with the planner.
- `check_orange.py` uses `import fitz`, which PyMuPDF 1.28.2 still supports with a deprecation notice. The pin keeps it working.

## How updates work

```
skills/                         generated; do not edit by hand (CI fails on hand edits)
conversion-manifest.json        per skill: source, method, converted and file hashes
versions.json                   every source bundle ingested, in order (hashes only)
tools/convert_skills.py         source bundle -> Claude skills with generic examples (standard library only)
tools/genericize.json           generic rewrites, keyed by the hash of each original line
tools/add_generic_rule.py       add a generic rewrite for a new or changed example line
tools/check_terms.py            fails on blocked brand, product, catalog or workbook terms
tools/blocked-terms.json        the blocked terms, stored as hashes only
tools/reconcile.py              compare a new bundle with the repo; --apply stages the update
tools/check_repo.py             repo integrity check (CI and the daily job run it)
tools/test_check_orange.py      self-test for the PDF check
```

The source bundles themselves are not stored here. A new bundle goes through `python3 -I tools/reconcile.py <bundle.zip>` (dry run), then `--apply`. The reconcile refuses a bundle whose skill files don't match the bundle's own manifest, a bundle older than the current one, and any run where `skills/` was edited by hand. When a new version adds or changes a workbook line or an acceptance example, the reconcile stops with exit code 7 until a generic rewrite is added with `tools/add_generic_rule.py`. To change a skill's wording, change it at the source or in the converter, never in `skills/`.

Maintained by Motif Platforms.
