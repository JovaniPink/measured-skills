# Fresh review of the 27 source decisions

Reviewed head: `6096f117dbffd86ed605bb9e0cef1f6def7612c1`, November 2, 2026.
This is a second owner review, not an independent reviewer or model evaluation.
The first fresh read of all 27 bodies matched their reviewed pins under the
unchanged checker. The complete online check also passed all 69 sources. The original failed
receipt, hold queue, observations and individual decisions remain in
[the source ledger](source-review-2026-11-02.json).

## Corrections

- The plugin specification has no retained earlier body. Its current content and
  changed entity tag are verified; saying that *only* the entity tag changed was
  unsupported. The ledger now states that historical content comparison is unavailable.
- PostgreSQL documents execution, side effects and a transaction example. The
  warning about external or nontransactional recovery is an evidence limit, not
  an additional guarantee attributed to that example.
- Google's latest-model page names a newer model. That does not prove the frozen
  Flash model is unavailable in Antigravity IDE. Keep its packet unchanged and
  verify the selected host and model before any separately authorized run.
- Commit `6096f117` bound the correct source and hashes but also edited two
  documentation files. The release process requires a manifest-only commit.
  Preserve both existing commits, commit this follow-up source first, then build
  the manifest from that clean HEAD and commit only the manifest. Read the exact
  resulting source from [the manifest](../../releases/0.19.0/manifest.json).

## Individual review

Numbers below identify records in the source ledger. The comparison covers
relevant authority content and affected skill contracts. Seventeen sources have
retained October 29 bodies; ten have no retained baseline. A current-content
review of those ten cannot establish historical semantic equivalence.

| Record | Authority | Fresh assessment and consequence |
| --- | --- | --- |
| 1 | Agent Plugins | Current package containment and optional components support the existing boundary; content delta unknown. Correct the overstatement. |
| 2 | Agent Skills | Retained document guidance matches; embedded deployment configuration changed. No canonical change. |
| 3 | Google managed agents | Official Markdown retains preview, egress, credential, oversight and inactivity-deletion limits. Keep hosted agents outside this trial. |
| 4 | Google latest model | New model guidance remains runtime-specific. Preserve the frozen trial; verify its actual host/model before execution. |
| 5 | Antigravity skills | Current discovery and manual invocation do not establish user-only enforcement. Keep all 17 explicit-only exclusions. |
| 6 | Terraform language | Retained visible guidance matches. Keep version and provider discovery. |
| 7 | OpenAI prompting | Current role, context and model-specific advice supports the non-executing prompt-review contract. Content delta unknown. |
| 8 | Google agent platform | Updated date differs; the retained platform grouping matches. No canonical change. |
| 9 | Cloud Storage metadata | Navigation and date changed; generation and metageneration retain separate meanings. No canonical change. |
| 10 | dbt incremental models | Retained guidance matches; retain adapter and incremental-strategy distinctions. |
| 11 | Spring Boot | Current version listings support project-version discovery, not a portable fixed version. No historical body. |
| 12 | OWASP initiative | Changed taxonomy/class ordering preserves the complete token multiset and page modification field. This remains resource-discovery evidence. |
| 13 | Git merge | Retained guidance matches. Preserve ancestry and the existing integration boundary. |
| 14 | Git worktree | Current shared-state, locking and removal rules support the existing assessment/reference. No historical body. |
| 15 | .NET | Retained landing-page guidance matches; discover the actual SDK and target framework. |
| 16 | Next.js upgrade | Displayed latest patch changed. Floating examples do not select an upgrade target. |
| 17 | OpenTelemetry | Retained signal guidance matches. Signal maturity and observed operation remain separate. |
| 18 | Claude prompting | Model-list and history wording changed. The prompt-review skill adopts neither model names nor API-history rules. |
| 19 | Python unittest | Three warning-example corrections do not contradict the test-review contract. No canonical change. |
| 20 | SLSA | Retained provenance guidance matches. Keep build and source provenance distinct. |
| 21 | Spark SQL | Current plans, statistics, joins and adaptive execution support version-specific diagnosis. No historical body. |
| 22 | Salesforce Apex | Banner and tutorial wording changed. Hosted limits and org-write authority remain unchanged in the skill. |
| 23 | Drupal | Retained visible guidance matches; keep testing, security and performance discovery. |
| 24 | PostgreSQL EXPLAIN | ANALYZE executes the statement. A transaction example does not establish universal recovery. No historical body. |
| 25 | PostgreSQL documentation | Current and prerelease listings remain distinct; the skill selects no version. No historical body. |
| 26 | Swift Evolution | Accepted proposals are future release goals. This script-loaded index does not bind individual proposal text or prove implementation. No historical body. |
| 27 | TypeScript | Retained visible guidance matches. Preserve project configuration and compiler-version discovery. |

## Two later changes at delivery

The next complete check found 67 matching and two changed sources. Keep that
[failed intermediate receipt](source-check-intermediate-2026-11-02.json).
Two fresh reads of each changed source then agreed. Comparing their full bodies
with the just-retained matching bodies found only:

- Next.js: the HTML deployment-ID attribute changed.
- OpenTelemetry: one Netlify RUM hosting script changed.

The bodies are otherwise identical after replacing those exact fields for this
comparison. That comparison is not a new freshness rule. The
[addendum](source-review-addendum-2026-11-02.json) binds both same-method repins
to the unchanged initial checkpoint; the
[closeout receipt](source-check-closeout-2026-11-02.json) records the later result.
The original 27-source test now checks its committed checkpoint, while two new
tests bind live pins to this addendum and reject unreviewed changes or weaker
policy. No historical record or test assertion is removed.

## Evidence limits and next boundary

The two original Google HTML addresses again redirect to AI Studio HTML without
a Last-Modified header. Their official Markdown endpoints return complete text
and match the reviewed content hashes. The web reader rejected their Markdown
content type; direct read-only HTTP retrieval supplied the complete responses.
No extraction or new normalization was added to the freshness check.

Four fresh raw bodies differ from the ledger's raw-body hashes while their
existing normalized fingerprints match. These are Google platform/storage,
Trailhead and Drupal. Raw-byte equality and normalized-marker equality remain
different claims. Publisher bodies and local comparison files stay private.

Only those two additional source pins change in this follow-up. Canonical and
packaged skills, invocation rules, global review date and maximum-age policy
remain unchanged. All 436 retained private
trial/preparation files still match their earlier hashes. Human usefulness,
current-source client acceptance, installation and supported-surface evidence
remain open. No new model task, billing change, installation, merge or release.
