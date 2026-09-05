---
name: lint-feasibility-assessment
description: Determine whether a proposed coding rule can be enforced reliably by an existing linter or a custom static-analysis rule, and recommend the narrowest alternative when it cannot.
---

# Lint Feasibility Assessment

Use this skill when someone asks whether a convention, design constraint, or test rule should be enforced by lint.

## Assessment workflow

1. Rewrite the request as a deterministic rule with an explicit scope: files, syntax, allowed forms, and exceptions.
2. Inspect the repository's formatter, TypeScript configuration, Oxlint/ESLint configuration, custom rules, and rule tests before proposing a new rule.
3. Classify the rule:
   - **Existing rule**: an enabled rule already enforces it.
   - **Custom static rule**: the requirement is visible in the AST and can be checked without executing the program.
   - **Partial enforcement**: lint can catch a syntactic subset, but semantic or cross-file cases need another check.
   - **Not a lint rule**: the requirement depends on runtime behavior, product meaning, visual comparison, external state, or human judgment.
4. For a custom rule, define the smallest node pattern that proves a violation. Specify whether it belongs in Oxlint, ESLint, TypeScript, Prettier, a test, or CI, and avoid overlapping an existing rule.
5. Validate the decision with rule tests containing at least one violation, one valid example, and the relevant boundary or exception. Do not add a rule merely because a single example looks undesirable.
6. Report false-positive risks, uncheckable cases, and the enforcement owner when lint is insufficient.

## Decision criteria

Prefer lint when the rule is local, deterministic, syntax-visible, fast, and stable under refactoring. Prefer TypeScript for type relationships, Prettier for formatting, tests for behavior and accessibility, and CI or review for repository-wide or contextual policy.

Do not recommend AST matching for a requirement that needs inferred business intent unless the project can state a safe syntactic proxy and accept its limitations. Do not use comments or naming conventions as proof of behavior.

## Output contract

Return:

- the classification and confidence (`enforceable`, `partial`, or `not suitable`),
- the exact rule boundary and affected files,
- the existing rule or proposed implementation location,
- valid and invalid examples,
- false-positive and false-negative risks,
- the verification command and any manual or runtime check that remains necessary.

If implementation is requested, make the smallest rule change, add focused rule tests, run the repository's formatting, type, lint, and test commands, and preserve unrelated configuration.
