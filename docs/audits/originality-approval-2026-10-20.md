# Exact candidate originality disposition for approval

Status: proposed; maintainer acceptance is pending. The originality hold remains.

Decision ID: `originality-018-owned-inventory-20261020`. Input revision: `64682fc047afffa3518ec97a03e5d85f09f1a2a9`.

## What is covered

The earlier [canonical expression packet](catalog-expression-disposition-2026-10-20.md) covers all 87 skills. This follow-up accounts for all 1713 tracked input files, including 1465 outside `skills/`. The [complete ledger](originality-approval-2026-10-20.json) binds file hashes, corrections, source families, retained artwork events, dependency observations, and explicit limits. It preserves the earlier packets without editing their historical results.

| Noncanonical family | Input files |
| --- | ---: |
| build-or-repository-control | 5 |
| catalog-schema-or-policy | 33 |
| developer-tool-or-test | 45 |
| documentation-or-instructions | 126 |
| fictional-example-or-projection | 5 |
| fixture-or-evaluation-record | 292 |
| generated-archive-or-checksum | 88 |
| generated-projection | 853 |
| owned-artwork | 1 |
| release-record | 17 |

The corrected payload adds three example notices and one regression test module. Proposal/acceptance documents and the final release manifest are separate decision records, excluded from the payload hash to avoid circular hashes. They must be bound by the exact submitted Git head and separately recorded proposal hash. All other tracked files are accounted for.

Input inventory SHA-256: `3dfe1db69b0cd4a0ffc7aa7041bb5dc6f01b74a1f62e3ac49db3d525d44251fe`.

Corrected payload SHA-256: `2f2e5fdf5405d423018e99f3ff81369107a1fbebc38b909e33038c516312c448`.

## Findings and repairs

- The copyable fictional overlay declared MIT but omitted the full notice. A failing regression reproduced this; canonical and both copied example notices now retain the root license. Actual private overlays do not inherit that license.
- The older Antigravity preview builder also omitted notices. A failing regression reproduced this; root and per-skill notices now appear in its file-hash receipt. Existing invocation restrictions remain.
- The README made an unsupported categorical no-copy claim. It now states the owned license offer, accurate methods, and review limits. SECURITY now describes actual metadata, notice, and artwork contents.
- The attribution checker now reports an attribution-pattern result and explicitly distinguishes it from originality qualification. Its detection logic is unchanged. The taxonomy summary no longer implies a current clean-room process.

## What the additional evidence establishes

The shared nine-line SVG equals a retained literal write and its owned Git creation. Two retained tool results report completion; an earlier failed attempt remains classified as unexecuted. All eleven generated copies match. Source and local rendering were inspected. It contains geometry, no embedded raster or font, and no external script/link. This supports lineage and copy consistency; no trademark search, outside-image comparison, or human-contribution determination was performed.

The inventory groups nongenerated assets by owned creation revision and retained MIT notice. Tool and fixture imports, credits, long content fields, attribution signals, package contents, and selected implementation paths were inspected. Detailed direct and targeted coverage is recorded in the ledger. This is complete file accounting plus bounded technical review, not a fresh independent line-by-line comparison of every document, test, and tool against outside works.

Publisher metadata was checked for all eight locked CI tools; each exact recorded wheel hash matched. Pinned license files for all three CI actions and the metadata-silent mypy_extensions version were inspected. Those programs are referenced by CI; their implementations are not bundled in this tree or skill archives. No dependency was installed, no wheel executed, and no comprehensive transitive binary-license audit was performed. Existing provenance pins and freshness policy were not changed.

Raw retained sessions and private source mappings remain private. Public event hashes identify privately retained evidence; automated tests do not retrieve or certify those private sessions. Owned Git history and a repository license offer cannot alone prove rights in every passage.

## Residual uncertainty and the policy decision

The historical corpus hold did not define a comparison corpus, threshold, accepted reviewer, or completion predicate. Earlier records also retained a further independent-review requirement. This proposal does not pretend those checks happened. It asks the maintainer to explicitly replace those requirements for this exact candidate with the documented technical review, accurate declarations and notices, and their informed acceptance. Keeping the former requirement instead means the hold stays open pending a separately scoped review.

The reviewer is Codex-assisted and overlaps with model-assisted authoring. No independent human or counsel opinion is recorded. Seventeen skills lack a located literal creation event, and the Swift profile creation trace is partial. Model training provenance, absence of prior exposure, passage-level human contribution, universal non-infringement, and exclusive copyrightability remain unestablished. These are disclosed limits, not passing test results.

The [MIT license](https://opensource.org/license/mit) preserves the copyright and permission notice. The Copyright Office distinguishes ideas and methods from expression in [Circular 33](https://www.copyright.gov/circs/circ33.pdf) and discusses human contribution and AI assistance in its [2025 report](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf). Those general sources do not decide ownership or infringement for this repository. This packet gives a technical evidence assessment, not a legal clearance opinion.

## Exact proposed decision

The following text is the decision requested. It is not an accepted decision.

> I accept the bounded owned-history, expression-review, and notice-retention evidence in originality-018-owned-inventory-20261020 for the exact submitted candidate, corrected payload hash, source commit, manifest commit, and proposal hash recorded with my decision. I accept its disclosed full inventory accounting and targeted manual/static review; I do not treat that work as a line-by-line independent outside comparison.
>
> For this 0.18.0 candidate only, I adopt that defined review plus my maintainer acceptance as the originality completion contract in place of the historical undefined originality-corpus gate and unspecified further independent-review requirement. I do not require an additional independent human/counsel review or outside-corpus comparison for this scoped decision. Those checks remain unperformed, not passing. This is an explicit policy choice accepting the recorded uncertainty, not a claim that independent legal clearance occurred.
>
> I retain the four supported owned adaptations, 83 original declarations after exposure, model-assistance limits, missing literal-write receipts, and unresolved passage-level human contribution. The repository offers only rights its contributors can grant under its retained MIT notices; this decision does not establish exclusive copyrightability, universal non-infringement, lack of prior exposure, trademark clearance, or a primary publisher's blanket prose-reuse permission.
>
> I accept the repaired notices in the Antigravity preview and fictional example, the shared SVG lineage and generated-copy evidence, and the distinction between referenced CI tools and bundled code. I do not authorize new third-party implementation imports, private-to-public promotion, or redistribution under an unsupported license. Credible conflicting expression or license evidence reopens the affected gate before further promotion.
>
> This approval changes only the named candidate's originality disposition. It does not approve billing changes, paid evaluations, client installation or qualification, merge, tag, publication, release, repository settings, or promotion. Fail-closed freshness, safety, provenance, private boundaries, independent behavioral case review, and receiving-client requirements remain. Future payload changes need a recorded delta review.

## How acceptance would be recorded

Only after explicit maintainer approval, append `docs/audits/originality-acceptance-0.18.0.json` with:

1. Decision ID, exact accepted text, owner, date, and approval evidence.
2. Submitted source commit, manifest-only commit, and final Git head.
3. Proposal JSON SHA-256 and corrected payload SHA-256.
4. Scope, exceptions, retained uncertainties, and triggers for renewed review.

Do not rewrite the preserved proposals as if earlier acceptance occurred. A changed payload requires a scoped delta review. Pending approval, no acceptance file is created and the hold remains. Approval here would settle only this candidate originality contract. Freshness, safety, independent behavioral-case review, actual client qualification, merge, installation, and release remain separate decisions. No billing change, paid evaluation, publication, or release is authorized.
