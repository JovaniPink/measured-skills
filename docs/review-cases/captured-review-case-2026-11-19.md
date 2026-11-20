# Captured review case: offline chooser layout and scope preservation

**Evidence type:** Captured read-only code review executed against a real,
public commit range in `JovaniPink/measured-skills`. Distinct from synthetic
teaching examples (such as the retry example in
[docs/code-review-workflow.md](../code-review-workflow.md)) and distinct from a
multi-user benchmark.

## Capture metadata

| Field | Value |
| --- | --- |
| Repository | `JovaniPink/measured-skills` (public) |
| Base revision | `92d24711d438bc0378f441f56079b52943333fa9` |
| Head revision | `42950f2dce740e828fad957db9a7d2a5991c2bb9` |
| Date captured | 2026-11-19 |
| Mode | Read-only static inspection of committed diff, surrounding callers, registry, and tests |
| Scope | `scripts/discovery-ui.js`, `scripts/discovery.py`, `tests/test_discovery.py`, `docs/audits/post-acceptance-delta-2026-10-20.json` |
| Actions prohibited during capture | No edits, no test execution, no commits, no pushes, no approvals, no merges |

## Intended behavior

Commit `42950f2dce740e828fad957db9a7d2a5991c2bb9` updates the offline discovery
chooser (`scripts/discovery-ui.js` and `scripts/discovery.py`) so form controls
stack cleanly inside `.controls`/`.field` containers with explicit `<label for>`
bindings, primary and recovery buttons maintain contrast, and open `<details>`
action scopes stay open when the user switches client, stack, or request style.

## Concise review packet

### 1. Supported finding

- **Finding ID:** `RC-20261119-01`
- **Severity:** `warning`
- **State against base:** `unchanged` (pre-existing mismatch in JS enhancement, preserved by the new `openScopes` initializer)
- **Location:** `scripts/discovery-ui.js:48` (comparing `scripts/discovery.py:352` and `docs/start.md:54`)
- **Failure:** In `scripts/discovery-ui.js:48`, `openScopes` seeds only single-mode
  routes (`data.routes.filter(r => r.modes.length === 1)`). The default route in
  `42950f2d:catalog/workflows.json` is `finish-work`, which has three modes
  (`assess`, `repair`, `maintain`). As a result, `finish-work:assess` renders
  collapsed on initial load whenever JavaScript runs, contradicting both the
  static HTML fallback (`scripts/discovery.py:352`, which sets `open` on
  `r['id'] == data['default_route'] and m['id'] == 'assess'`) and
  `42950f2d:docs/start.md:54` ("**Find out what remains - no edits**, which is
  already expanded in the chooser.").
- **Evidence:** Direct inspection of `42950f2d:scripts/discovery-ui.js:48`,
  `42950f2d:scripts/discovery.py:352`, `42950f2d:catalog/workflows.json`
  (`default_route: "finish-work"`), and `42950f2d:docs/start.md:54`. The new
  regression test in `42950f2d:tests/test_discovery.py:415-424` did not catch
  this because it manually toggled `choice-review`'s `assess` scope and never
  asserted the initial `open` state of `choice-finish-work`.
- **Impact:** First-time offline users opening the interactive chooser must
  search for and open the default read-only assessment that the getting-started
  guide says is already expanded.
- **Suggested direction:** Seed `${data.default_route}:assess` into `openScopes`
  in `scripts/discovery-ui.js` and assert `defaultInitiallyOpen === true` in
  `tests/test_discovery.py`.

### 2. Plausible concern cleared by counter-evidence

- **Item ID:** `RC-20261119-02`
- **Initial concern:** Replacing implicit `<label>` wrappers with explicit
  `id`/`htmlFor` pairs (`discovery-search`, `discovery-client`, `discovery-stack`,
  `discovery-style`) in `scripts/discovery-ui.js:17-40` and adding a global
  `button{background:#125d48;color:#faf8f3}` rule in `scripts/discovery.py:370`
  could collide with existing route IDs in the DOM or break contrast on the
  secondary zero-results recovery buttons.
- **Competing explanation tested:** Whether any route ID in `catalog/workflows.json`
  or element in `#static-guide` shares a `discovery-*` ID, and whether CSS
  cascade order lets `.recovery-actions button` override the base `button` rule.
- **Resolving evidence:**
  - All 21 route IDs in `42950f2d:catalog/workflows.json` (`finish-work` through
    `learn-release`) were inspected; none uses a `discovery-` prefix, and
    `#static-guide` (`scripts/discovery.py:351-356`) emits no form controls or
    `discovery-*` IDs.
  - In `42950f2d:scripts/discovery.py:370-372`, `.recovery-actions button`
    (specificity `0,1,1`) appears after `button` (`0,0,1`) and explicitly sets
    `background:#fff;color:#172c27;border-color:#6b7f75`.
- **Bounded conclusion:** Both ID-collision and recovery-button-contrast concerns
  are **cleared** for revision `42950f2dce740e828fad957db9a7d2a5991c2bb9`. Do not
  add defensive wrapper prefixes or inline styles solely to satisfy this lead.
  Reopen only if a future route adds a `discovery-*` ID or introduces a third
  button variant.

### 3. Unresolved question and explicit coverage gap

- **Item ID:** `RC-20261119-03`
- **Question:** When `dist/discovery/index.html` is opened directly from local
  disk over `file://` under its Content Security Policy (`default-src 'none';
  script-src 'unsafe-inline'; style-src 'unsafe-inline'`), does clipboard copy
  either succeed or fall back cleanly to `pre.focus()` across Safari, Firefox,
  and Chrome, and do screen readers reliably announce status text after the
  `role="status"` node is moved in the DOM (`host.append(status)` at
  `scripts/discovery-ui.js:56` and `copy.after(status)` at `:97`) immediately
  before mutating `status.textContent`?
- **Why unresolved:** `42950f2d:tests/test_discovery.py:330-437` runs
  `discovery-ui.js` in a synthetic Node `vm` stub (`makeEl`) with synchronous
  `dispatch('toggle')` and mocked `navigator.clipboard.writeText`. Earlier
  Playwright checks inspected the HTTP-served copy on `localhost`, not `file://`
  downloads or live VoiceOver/NVDA speech output.
- **Next check:** Test a saved local copy of `dist/discovery/index.html` over
  `file://` in target browsers and verify live-region announcements with an
  actual screen reader before claiming full offline accessibility parity.

## Five-dimension state ledger

| Item | Investigation coverage | Claim assessment | Disposition | Verification (at reviewed revision) | Completion |
| --- | --- | --- | --- | --- | --- |
| `RC-20261119-01` (default route initial open state) | `examined` | `supported` | `accept` (owner accepted in follow-up slice; see note below) | Static inspection of `42950f2d` source, fallback HTML generator, registry, and docs; no test run during capture | Complete for read-only review |
| `RC-20261119-02` (`discovery-*` IDs and `.recovery-actions button` contrast) | `examined` | `cleared` | `reject` (no code change needed) | Static inspection of all 21 route IDs in `42950f2d:catalog/workflows.json` and CSS rules in `scripts/discovery.py:368-372` | Complete for read-only review |
| `RC-20261119-03` (`file://` clipboard fallback and reparented `role="status"` announcements) | `blocked` (no `file://` browser or screen-reader run in read-only capture) | `unresolved` | `defer` (manual browser and AT check required) | None executed at `42950f2d`; Node `vm` stub does not cover real browser CSP/`file://` or screen-reader trees | Complete with gap explicitly retained |

## Follow-up note (separate from read-only capture)

After this read-only review of `92d24711..42950f2d`, the owner accepted
`RC-20261119-01` as a separate repair in the `codex/review-evidence-workflow-20261119`
branch by seeding `${data.default_route}:assess` into `openScopes` in
`scripts/discovery-ui.js` and adding a `defaultInitiallyOpen` assertion to
`tests/test_discovery.py`. `RC-20261119-03` remains open and is not marked
cleared by that unit test.
