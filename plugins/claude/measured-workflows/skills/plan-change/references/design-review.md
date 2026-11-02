# Understand a design before implementing it

First reconstruct the proposal in plain language: users, inputs, state owners,
transitions, outputs, failure behavior, and the decision the document supports.
Cite its current revision and the approved requirements. A document titled
"design" may be a proposal, a historical decision, or a current contract.

Compare that reconstruction with actual callers and constraints. Ask what existing
capability could satisfy the outcome, what the smallest coherent change is, and
what happens if the change is not made. Do not manufacture an adversarial review
or demand a redesign simply to produce findings.

Check assumptions, reuse, alternatives, permissions, compatibility, partial
failure, retries, recovery, and observable acceptance. Separate decisions needed
before implementation from details the implementing owner can safely discover.
A missing acceptance condition matters more than a preferred document template.

Self-review is useful. An independent reader is optional unless required by the
user: it needs explicit delegation, suitable context access, and an authorized
billing route. Give that reader the identified document and necessary public
contracts; ask for a reconstruction and concrete uncertainties, not approval.
Do not launch reviewers from this read-only planning instruction.

When a reconstruction differs, distinguish an unclear document, failed or partial
read, unavailable prerequisite, and reviewer error. A misunderstanding alone does
not prove the document is defective. Preserve the existing three-round budget
when this is part of a bounded review; new evidence does not reset it.

Return the reconstructed behavior, material findings, implementation-ready parts,
and unresolved decisions. Do not execute the design or treat a model's verdict
as human approval.
