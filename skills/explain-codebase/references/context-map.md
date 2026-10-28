# Build one useful context map

Use a map when a later session needs to find the same behavior. Bound it to the
requested module or journey; an exhaustive directory inventory usually obscures
what matters. This is source inspection, not a context compiler or a token-saving
measurement.

1. Identify repository, exact revision, relevant staged/working/untracked changes,
   and the question the map answers. Hash relevant uncommitted inputs if the map
   will be reused. Do not collect unrelated or sensitive files.
2. Trace entrypoints to state owners and downstream effects. Cite real paths and
   symbols for interfaces, callers, configuration, persistence, and failure paths.
3. Separate canonical sources, generated projections, tests, fixtures, and proposed
   designs. Identify the authority for each important state transition.
4. Find check commands in repository instructions and configuration. Label commands
   as discovered, executed, or unavailable; a discovered command is not a result.
5. Include unknowns and a small list of triggers for rereading the map: changed
   source revision, relevant configuration, contract, or ownership.

Return the map in the answer by default. Save one document only when the user has
authorized documentation edits, using the project's existing convention. Do not
create recursive README files or edit AGENTS.md to make the map authoritative.
A map remains a dated explanation and cannot grant tools or permissions.

Synthetic example: a save request enters `saveDraft`, validates an identifier,
and calls `DraftStore`. The map cites those symbols and their error tests. With
no runtime receipt, it says that the source describes persistence, not that a
user's draft was observed to survive a restart.
