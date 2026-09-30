---
name: finding-consolidation
description: Merge findings from several completed reviews into one ranked list by assigning each root cause a single owner, regrading onto one severity scale, and disclosing what was cut. Use when two or more reviews have already reported on the same artifact and their findings overlap, repeat, or rank differently; not for running a review or for consolidating command results.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-skills"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Finding Consolidation

Merge findings that several reviews already produced. This workflow reads reported findings; it does not run a review, reopen an artifact, or replace a skill's own judgment.

## Preconditions

Two or more completed reviews with their findings, the artifact they reviewed, and the revision each review used. If the reviews used different revisions, say so and consolidate only what the shared revision supports.

## Workflow

1. Record each source review, the skill that produced it, its revision, and its scope. A finding whose source cannot be named stays unconsolidated.
2. Group findings by root cause rather than by symptom, wording, or location. Two reports of one cause are one finding.
3. Assign each group a single owner: the skill that owns the underlying rule. Another skill's report of the same cause becomes an observed effect attached to that finding, naming the skill that saw it.
4. Regrade every finding onto one severity scale: `none`, `note`, `warning`, or `error`. When sources disagree, keep the highest severity any source supports and record the disagreement.
5. Carry a finding state only where the source review pinned a change. Do not infer a state from a review that examined a system, a package, or a corpus.
6. List every confirmed location inside its single finding. Do not emit one finding per location.
7. Rank by reader impact. When the list is longer than a reader can act on, report the top findings and state how many were held back and where they are.
8. Name what no source covered. Consolidation cannot close a gap that no review examined.

## Boundaries

- Do not raise or lower a severity to make a list look balanced. A regrade needs a stated reason.
- Do not merge findings whose causes differ because their locations match, and do not split one cause because two skills used different words.
- Do not treat a consolidated list as a verdict, an approval, or evidence that the artifact is safe outside the reviewed scope.
- A skill that reports a disposition rather than a severity keeps it. Record it beside the severity instead of converting it.
- Consolidating does not re-run anything. An unavailable source review stays unavailable and is named.

## Output

Lead with the ranked findings, most severe first. For each finding provide `Severity`, `State`, `Owner`, `Locations`, `Cause`, `Evidence`, and `Observed by`. Then report `Sources`, `Disagreements`, `Held back`, and `Uncovered scope`. If no finding survives consolidation, say so and name the reviews that reported nothing.
