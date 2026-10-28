# Coverage Fanout

Use coverage fanout when one artifact must be inspected through independent, non-overlapping lenses.

1. Define the exact artifact and shared revision.
2. Assign distinct coverage dimensions, such as security, accessibility, compatibility, performance, or test quality.
3. Keep file ownership read-only unless each writer has an isolated target.
4. Require findings to include location, scenario, evidence, severity, and uncertainty. Grade severity as `none`, `note`, `warning`, or `error`.
5. Deduplicate overlapping findings and reconcile conflicting conclusions against the artifact.
6. Run integration validation after any accepted changes.

Fanout increases coverage, not authority. A worker report is a lead until the integration owner verifies it.
