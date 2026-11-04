# Playbook: review

> Owns: auditing a diff or a finished spec against the contracts · Not here: changing code; a review only reports

## Steps

1. Read the diff (`git diff main...HEAD`, or the staged and unstaged changes) and the active spec.
2. Check it against each contract and cite file and line for every finding:
   - ENGINEERING.md: an abstraction with one user; a unit with two responsibilities; a vendor called directly from business logic with no stated exception; a choice resting on an outside fact with no cited source.
   - ARCHITECTURE.md: a dependency that crosses a layer the wrong way.
   - TESTING.md: a requirement without a test; a test that cannot fail; branching in a test body; a mocked unit under test; a skipped or weakened test.
   - DESIGN.md: tokens, copy or interface shapes outside the rules.
   - Docs: behavior changed but the contract that describes it did not.
3. Report findings by severity, with file and line. Change nothing; the user decides.
