# Focused checks

Primary documentation: [official Salesforce Apex fundamentals](https://trailhead.salesforce.com/content/learn/modules/apex_database/apex_database_intro). For fuller language coverage, consult the [official Apex Developer Guide](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_apex_developer_guide.pdf); for client components, consult the [official Lightning Web Components guide](https://developer.salesforce.com/docs/platform/lwc/guide).

## Discovery

Inspect `sfdx-project.json`, package directories and aliases, dependency declarations, API versions, metadata and destructive-change manifests, org-shape assumptions, Apex, Lightning Web Components, permissions, CLI configuration, Node metadata, and CI scripts. Do not read local credential stores while discovering the project.

## Judgment focus

Review bulk behavior, governor limits, sharing, object and field permissions, query and DML placement, transactions, callouts, asynchronous work, recursion controls, test isolation, client-server contracts, reactive state, cache behavior, browser security, accessibility, and permission-aware data access.

## Gate families

Consider repository static analysis, formatting, linting, local unit tests, metadata consistency, package checks, and builds. Org-backed validation, scratch-org creation, package installation, tests, deployment, permission assignment, and destructive changes require separate exact authority.

## Compatibility

Check API versions, package dependencies, namespaces, org features, metadata types, Apex and LWC contracts, permissions, deployment order, and destructive manifests. Record unavailable tools and org evidence explicitly; never manufacture a passing result.
