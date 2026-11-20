# Disconfirmation and failure cases

**Evidence type:** Synthetic and reconstructed teaching cases. None of these
snippets is raw production code or an executed client benchmark. Each case
teaches the same review question: *what competing explanation could produce this
observation, and what evidence distinguishes it from the claimed defect?*

---

## Case 1: Authorization enforced below the changed handler (false alarm cleared)

- **Requirement and code:** An API handler `GET /projects/{id}` is refactored to
  remove an inline `if project.org_id != user.org_id: raise Forbidden()` check
  and calls `project_repo.get_for_actor(actor, project_id)` directly.
- **Tempting initial interpretation:** "Removing the tenant check in the handler
  opens a cross-tenant IDOR vulnerability."
- **Missing contract or competing explanation:** The repository helper
  `get_for_actor` might enforce tenant ownership in the SQL predicate or via
  row-level security, making the handler check redundant rather than missing.
- **Resolving observation:** Reading `project_repo.get_for_actor` shows
  `WHERE id = :project_id AND org_id = :actor_org_id` with a required non-null
  `actor.org_id` assertion, plus an integration test where an actor from org B
  requests an org A project and receives `404`.
- **Bounded conclusion:** The cross-tenant exposure claim is **cleared** for
  this handler path under the inspected repository contract. Keep a separate
  note only if another caller invokes an unscoped `get_by_id` method or bypasses
  `get_for_actor`.
- **Regression pointer:** Paired with `rc-02-auth-enforced-below` (and contrasted
  with `rc-01-missing-tenant-scope` and `rc-08-missing-store-contract`) in
  [evals/review-comparison-v1](../../evals/review-comparison-v1/README.md).

---

## Case 2: Next.js cache scope and principal boundary (defect vs. cleared path)

Concrete illustration of the trace required by
[review-nextjs-cache-auth](../../skills/review-nextjs-cache-auth/SKILL.md):
principal -> authorization boundary -> data ownership -> cache scope ->
invalidation.

- **Requirement and code:** A dashboard Server Component displays an
  organization's invoice summary. A patch wraps `fetchInvoiceSummary(orgId)` in
  `unstable_cache(fn, ["invoice-summary"])` (or a shared cache directive without
  binding the principal/org key) to cut database load.
- **Tempting initial interpretation:** Either "caching speeds up the route, LGTM"
  (missed defect) or "never cache authenticated routes" (over-broad objection).
- **Missing contract or competing explanation:** Safe caching depends on whether
  the cache key partitions strictly by authorized tenant/principal scope and
  whether writes invalidate that exact tenant tag.
- **Resolving observation:**
  - *Defect path:* The cache key is static (`["invoice-summary"]`), while `orgId`
    is closed over without entering the key. Organization B receives
    Organization A's cached invoice summary after a warm hit, and invoice updates
    do not call `revalidateTag(\`invoices:${orgId}\`)`.
  - *Cleared path:* The key includes the verified session `orgId` (and role
    tier if fields vary by role), the data layer still checks membership before
    filling the cache, and mutations invalidate `invoices:${orgId}`.
- **Bounded conclusion:** Report the cross-tenant cache leak as `error` when the
  key omits the principal/tenant boundary; clear the cache-leak claim if key
  partitioning, authorization before fill, and tenant-scoped invalidation are
  verified together (while keeping uninspected CDN/proxy headers as an explicit
  coverage boundary).
- **Regression pointer:** Use an authenticated two-tenant request test asserting
  that Tenant B never observes Tenant A's payload and sees updated totals after
  Tenant B's mutation.

---

## Case 3: Tests pass without exercising the changed contract

- **Requirement and code:** A patch updates `validate_webhook_signature(raw_body,
  header, secret)` to reject expired timestamps older than 5 minutes. The PR
  adds a unit test that passes in CI.
- **Tempting initial interpretation:** "CI is green and a new timestamp test was
  added, so replay protection is verified."
- **Missing contract or competing explanation:** The test might mock the clock
  or validator helper in a way that bypasses the real signature/timestamp branch,
  making the assertion pass even when the guard is deleted.
- **Resolving observation:** Reading the test shows
  `patch("app.webhooks.verify_timestamp", return_value=False)` paired with a
  mocked handler response, so the actual comparison in
  `validate_webhook_signature` never executes during the test.
- **Bounded conclusion:** Mark the missing behavioral verification as a
  **supported** test-quality finding (`warning` or `error` depending on risk),
  citing exact lines in the test file. Do not confuse "a test exists and ran
  green" with "the replay guard was exercised."
- **Regression pointer:** Paired with `rc-04-tautological-test` in
  [evals/review-comparison-v1](../../evals/review-comparison-v1/README.md).

---

## Case 4: Mixed-version rollout incompatibility outside the diff

- **Requirement and code:** A worker service changes a queued job JSON payload
  from `{"status": "queued"}` to `{"status": "pending_dispatch"}` and updates
  the worker's own consumer enum in the same PR. All unit tests pass.
- **Tempting initial interpretation:** "Producer, consumer, and tests all match
  in this commit, so the rename is safe."
- **Missing contract or competing explanation:** During a rolling deployment, an
  old consumer instance (revision N-1) can read messages written by a new
  producer (revision N), or a new consumer can read already-queued messages from
  before the deploy.
- **Resolving observation:** Inspecting the consumer's deserializer shows strict
  enum parsing with no fallback for unknown values and no two-phase expand/
  contract rollout (accepting both `"queued"` and `"pending_dispatch"` first).
- **Bounded conclusion:** Report a **supported** compatibility finding (`error`
  for rolling deployments) explaining the N-1/N skew window. If the deployment
  contract instead guarantees queue drain during maintenance downtime, keep the
  finding conditional on that operational contract and verify it with the owner.
- **Regression pointer:** Paired with `rc-05-mixed-version-rollout` in
  [evals/review-comparison-v1](../../evals/review-comparison-v1/README.md).
