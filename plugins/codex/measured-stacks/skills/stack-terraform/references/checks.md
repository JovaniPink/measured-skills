# Focused checks

Primary documentation: [official Terraform Engineering Profile reference](https://developer.hashicorp.com/terraform/language). Verify version-sensitive behavior against the repository's pinned toolchain.

## Discovery

Inspect Terraform files, module structure, required providers, dependency lockfiles, backend declarations, workspaces, and repository scripts. Resolve nested modules, workspaces, generated sources, and CI commands before selecting gates.

## Judgment focus

Review resource-address churn, unsafe `for_each` keys, sensitive state, provider defaults, lifecycle misuse, implicit dependencies, broad IAM, replacement, and drift.

## Gate families

Consider repository scripts, formatting, initialization with controlled backend behavior, validation, static analysis, policy checks, and reviewed plans without applying. Run only commands supported by repository evidence and the current authorization boundary.

## Compatibility

Check Terraform and provider versions, module interfaces, state moves, import blocks, backend behavior, upgrade guides, and plan changes across environments. Record unavailable tools and environments explicitly; never manufacture a passing result.

