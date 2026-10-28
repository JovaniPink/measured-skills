# Work Packages

Use work packages when a plan must be divided across reviewable units or owners.

Each package names:

- Outcome and excluded work.
- Inputs and exact dependencies.
- Owned files, interfaces, or read-only scope.
- Expected behavior and acceptance evidence.
- Tests and integration gates.
- Rollout, rollback, and stopping conditions.
- Decisions that remain with the integration owner.

Order packages by real dependency. Do not manufacture parallelism, and do not make a package independently mergeable when its contract cannot be verified alone.
