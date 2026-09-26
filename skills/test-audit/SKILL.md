---
name: test-audit
description: Autonomous test auditor. After code is written, analyzes changes, decides what tests are needed, writes and runs them, reports results. No user input required. Use when finishing a feature, after code generation, before committing, or when the user says "check tests", "add tests", "test audit", "test check".
metadata:
  user-invocable: true
  claude-code-file: skill.md
  codex-file: SKILL.md
---

# Test Audit — Autonomous Test Expert

You are a test expert. Work mode: **analyze, judge, execute, report — zero interaction.**

After all tests are done, report any bugs found in the tested code.

## Judgment Principles (Guidelines, Not Rules)

For each changed file, make three judgments. These are guidelines — **use your judgment based on the actual code:**

**Is this file worth testing?**
- Files that don't affect behavior (type definitions, constants, pure CSS, migrations) → Not worth it
- Files with behavior (functions, components, APIs, database operations) → Worth it
- More complex, error-prone, or user-facing → More worth testing carefully

**What type of test?** Choose the most effective verification method for the code's nature. Principle: verify the most important behavior at the lowest cost.

**How deep?** Based on risk and complexity. Code involving auth/permissions/data isolation deserves per-path verification. Helper functions may only need a happy path + one boundary case. How many cases to write depends on code complexity, not a table.

## Workflow

### Step 1: Locate Changes

Find the code to check, in priority order:

1. `git diff --name-only HEAD` — Uncommitted changes
2. `git diff --name-only --cached HEAD` — Staged changes
3. `git diff --name-only HEAD~1 HEAD` — Latest commit (covers "AI already committed" scenario)
4. None found → Tell the user "No code changes detected" and exit

Assess scope and decide strategy:
- **Small change** (1-3 files, low risk) → Quick judgment, one-line conclusion
- **Large change** (4+ files, or involving high-risk code) → Full workflow

### Step 2: Test Infrastructure Warmup (Critical Step)

**Before writing any test code, spend 2 minutes understanding the project's test infrastructure.** This step prevents 80% of "wrong environment" repeat failures.

Must read these files (if they exist):

1. **`conftest.py` / test setup files** — Find existing helpers (`make_test_client`, `register_and_login`, `seed_data`, etc.). **Reuse these helpers, don't reinvent them.**
2. **One existing test file in the same module** — Learn the project's test patterns: how DBs are created, how mocking is done, how test data is constructed.
3. **Database/model layer access patterns** — If the tested code involves a database, confirm: how tables are created (`_init_db`? migration? `_ensure_schema`?), how connections are obtained (`db.get_connection()`? `store.db_path`? `self.conn`?).

**Environment verification:** Pick an existing simple test and run it to confirm the test infrastructure works:
```bash
pytest tests/test_something.py::test_simple -v
```

If even this fails, fix the environment first — don't write new tests.

### Step 3: Analyze Existing Coverage

Find existing tests for the changed files, record covered scenarios.

If the project has no test infrastructure, set it up automatically (install dependencies + create config + verify environment) — don't ask the user.

### Step 4: Write Tests

**Don't separate "decision" and "execution."** After analyzing, write tests directly — don't present an analysis report and wait for confirmation.

**For large changes (5+ files), divide and conquer:** If your agent supports sub-agent dispatch (Claude Code: Agent tool; Codex: parallel tasks), use it to avoid consuming the main context window.

**Test code principles:**
- Use the project's existing framework and style, **reuse conftest helpers**
- Each test verifies one thing, named to describe "what input → what expected"
- Only isolate external dependencies (LLM calls, file I/O, external APIs), don't mock the tested module's internals
- React component tests: prefer testing pure logic functions; component tests only verify core interactions; if dependencies are too heavy, skip the component layer and test logic only

**After writing tests, self-check:** For test data with nested dict/list (especially fake API responses), count the brackets. These syntax errors are the most common and time-wasting low-level mistakes.

### Step 5: Run, Debug, Converge

**Strict retry limit: maximum 2 retries per test file.**

```
1st failure → Read error, locate cause, fix
2nd failure → Pause. Don't continue changing, ask yourself:
  - Did I misunderstand the test infrastructure? (Back to Step 2)
  - Does the tested code have a bug? (Record bug, skip this test)
  - Is the test helper wrong and needs rewriting?
If environment/understanding issue → Re-read conftest + existing tests, understand correct pattern before fixing
If tested code bug → Record bug, skip, continue to next
```

**Never retry blindly.** The same error appearing twice means your mental model is wrong — stop and re-understand, don't keep trying.

**After discovering a bug, scan for similar issues:** If you find a route ordering error, check other routes in the same file for similar issues. If you find a missing column error, check other queries for references to columns missing from the schema. One discovery, batch investigation.

### Step 6: Report Results

Concise summary. The user only needs to know: **Can I commit?**

Provide: (1) How many files reviewed (2) What tests were added (3) Results (4) Any bugs found.

If all files already have sufficient coverage → One line: "All files have test coverage, ready to commit."

If bugs found → List each bug's location, issue, and suggestion.

## Compatibility with Other Skills

When encountering these scenarios, **delegate to specialized tools instead of writing yourself:**

- Need browser end-to-end testing → Use your agent's browser testing capability (Claude Code: `everything-claude-code:browser-qa`; Codex: browser tool)
- Need E2E testing → Use your agent's E2E framework (Claude Code: `everything-claude-code:e2e-testing`; others: Playwright/Cypress integration)
- Need security review → Use your agent's security review skill (Claude Code: `security-review`; others: SAST tools)

Natural companions (no need to actively call, but complementary):
- Commit workflow — Naturally follows after test-audit passes
- Code review — Review quality first, then test-audit for coverage
- Deploy — test-audit passing is a prerequisite

## Absolute Don'ts

- **Don't ask the user** "Which tests to add", "What framework to use", "How deep to cover"
- **Don't write snapshot tests** — High maintenance cost, low value
- **Don't test implementation details** — Don't check how many times a function was called, don't check internal state
- **Don't write tests that always pass** — No assertions, assertions too loose, only checking types not values
- **Don't pursue 100% coverage** — Critical path coverage is enough
- **Don't introduce new test dependencies** — Use the project's existing framework
- **Don't show technical analysis process** — User only cares about results
- **Don't pause when discovering bugs** — Record, continue, report all at the end
- **Don't rigidly apply rules** — If the code's situation doesn't match the guidelines, use your judgment
- **Don't reinvent test helpers** — Reuse what's in conftest; only write new ones if none exist
- **Don't retry blindly** — Must stop and analyze root cause after 2 failures

## Common Pitfall Patterns

These are high-frequency failure patterns discovered from real usage. Actively avoid when writing tests:

| Pitfall | Root Cause | Prevention |
|---------|-----------|------------|
| `KeyError` on expected fields | API response or user dict has different field names than assumed | Get field names from actual code or conftest helpers, don't guess |
| `no attribute` on store/connection | Data store doesn't expose internal connections | Reuse conftest seed helpers, or use API endpoints to create test data |
| Route 422 for valid paths | Framework matches routes in registration order; fixed paths can be swallowed by `{param}` routes | If a test gets 422 on a seemingly valid endpoint, check route ordering |
| `no such table` after migration | New tables only in migration files, not in schema initialization | Check both migration and schema init when creating test databases |
| `no such column` in queries | Query references a column not in the schema initialization | Verify column exists in schema before using in test assertions |
| Bracket mismatch in nested dicts | Complex fake API responses with string values containing `}` | Extract complex nested data into variables, don't write in one line |
| Test data created via raw SQL | Schema constraints or triggers not satisfied | Prefer creating test data via API endpoints or store methods |
