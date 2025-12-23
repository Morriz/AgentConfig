# Testing Directives

Purpose: Define testing standards and quality gates - not implementation details. Apply in every project unless configuration explicitly overrides.

## 1. Pre-Commit Quality Gates

1. **All tests MUST pass** before committing code.
2. **All linting errors MUST be fixed** before committing code.
3. **All type checking errors MUST be resolved** before committing code.
4. Never commit code with failing tests, lint violations, or type errors.
5. If pre-commit hooks are configured, they MUST pass without warnings.

### **CRITICAL: Run Targeted Tests, NOT Full Suite During Development**

**NEVER waste time running the entire test suite when you know which specific tests are affected.**

When fixing bugs or making changes:

1. **Run ONLY the specific failing test(s)** - not the entire suite
2. **Use test file/module paths** - `uv run pytest tests/unit/test_foo.py -v`
3. **Run single test methods** - `uv run pytest tests/unit/test_foo.py::TestClass::test_method -v`

**Examples:**

```bash
# ✅ CORRECT - targeted test after fixing file_handler.py
uv run pytest tests/unit/test_file_handler.py -v

# ✅ CORRECT - single failing test
uv run pytest tests/integration/test_file_upload.py::TestFileUploadFlow::test_file_upload_without_claude_code -v

# ❌ WRONG - running entire suite when you know which test failed
make test  # DON'T do this during active debugging
```

### **CRITICAL: Always Use Parallel Execution with Bash Timeout**

**Every multi test invocation MUST include:**

- `-n auto` for parallel execution (pytest-xdist)
- **Bash tool timeout based on test type:**
  - **Unit tests: 3000ms (3s)** - fast, parallel, should complete quickly
  - **Integration tests: 15000ms (15s)** - slower, involve I/O and real systems

**Examples:**

```bash
# ✅ CORRECT - unit tests with 3s timeout
uv run pytest -n auto tests/unit/test_foo.py -v  # Use timeout=3000 in Bash tool

# ✅ CORRECT - integration tests with 15s timeout
uv run pytest -n auto tests/integration/test_file_upload.py -v  # Use timeout=15000 in Bash tool

# ❌ WRONG - no parallel execution
uv run pytest tests/unit/test_foo.py -v

# ❌ WRONG - wrong timeout for test type
uv run pytest -n auto tests/unit/test_foo.py -v  # Using timeout=15000 (too long!)
```

**NEVER waste time waiting for tests - always use `-n auto` for multiple tests and appropriate timeout (3s for unit, 15s for integration).**

## 1. Test Organization

1. One test file per source module (e.g., `foo.py` � `test_foo.py`).
2. Group related tests in the same file.
3. Use descriptive test function names that explain the expected behavior.
4. Test files go in a dedicated `tests/` directory.
5. Mirror source structure in test directory when helpful.

## 2. Test Quality

1. **Test behavior, not implementation** - tests should validate outcomes, not internal mechanics.
2. **One assertion per test** - focus each test on a single expected outcome.
3. **Arrange-Act-Assert pattern** - set up, execute, verify.
4. **No logic in tests** - avoid conditionals, loops, or complex calculations.
5. **Tests must be deterministic** - same input always produces same output.
6. **Fast tests** - keep unit tests under 100ms each when possible.

## 3. Test Coverage Priorities

1. **Edge cases over happy paths** - boundary conditions are where bugs hide.
2. **Error conditions** - test all error paths and exception handling.
3. **Integration points** - test boundaries between systems/modules.
4. **Public interfaces** - test exported functions, classes, and APIs.
5. **Do NOT test private methods** - they're implementation details.

## 4. Mocking & Dependencies

1. Mock at **architectural boundaries**, not internal functions.
2. Use real objects for simple dependencies.
3. Stub external services (APIs, databases, file systems).
4. **Never mock what you don't own** - wrap third-party code in adapters.
5. Avoid over-mocking - it couples tests to implementation.

## 5. Test Naming

1. **Format**: `test_<function>_<scenario>_<expected_outcome>`
2. **Examples**:
   - `test_calculate_total_with_empty_cart_returns_zero`
   - `test_authenticate_with_invalid_token_raises_error`
   - `test_send_email_with_missing_recipient_fails`
3. Names should read like documentation.

## 6. Fixtures & Setup

1. Use test framework fixtures for shared setup (pytest fixtures, unittest setUp).
2. Keep fixtures focused and composable.
3. Avoid fixture interdependencies.
4. Clean up resources in teardown/finalizers.
5. Prefer factory functions over complex fixtures.

## 7. Assertions

1. Use specific assertions that provide clear failure messages.
2. **Python**: `assert actual == expected, "Clear message"`
3. **TypeScript**: `expect(actual).toBe(expected)`
4. Compare exact values, not types or truthiness.
5. Fail fast with clear diagnostics.

## 8. Linting & Type Checking

1. **Run linters before committing** - fix all violations.
2. **Run type checkers before committing** - resolve all errors.
3. **Never suppress lint/type errors** unless absolutely necessary and documented.
4. Common lint violations that MUST be fixed:
   - Unused imports
   - Unused variables
   - Import ordering violations
   - **Import-outside-toplevel violations** (all imports at module level)
   - Missing type annotations
   - Overly complex functions
5. Type checking errors that MUST be resolved:
   - Missing return type annotations
   - Missing parameter type annotations
   - Generic types without parameters (`dict` � `dict[str, Any]`)
   - Use of `Any` without justification
   - Incompatible type assignments

## 9. Test Isolation

1. Each test runs independently - no shared state between tests.
2. Tests can run in any order.
3. Use fresh instances/data for each test.
4. Use mocks for all deps / boundaries to focus on code under test.
1. Reset mocks between tests.
2. Clean up global state in teardown.

## 10. Testing Anti-Patterns to Avoid

1. **Flaky tests** - non-deterministic tests that pass/fail randomly.
2. **Slow tests** - tests that take seconds to run (indicates integration, not unit).
3. **Testing implementation details** - tests that break when refactoring.
4. **Over-mocking** - mocking everything makes tests brittle.
5. **Mega tests** - one test that validates many behaviors.
6. **No assertions** - tests that execute code but don't verify outcomes.
7. **Commented-out tests** - either fix or delete them.

## 11. Continuous Integration Standards

1. All tests run on every commit.
2. Tests must pass before merging to main branch.
3. Linting and type checking run automatically.
4. No commits with `--no-verify` to bypass hooks.
5. Keep test suite fast (< 10s for unit tests).

## 12. Pre-Commit Checklist

Before committing code, verify:

- [ ] All tests pass (`make test` or equivalent)
- [ ] All lint violations fixed (`make lint` or equivalent)
- [ ] All type errors resolved (`make lint` or mypy/tsc)
- [ ] No unused imports or variables
- [ ] All imports at top level (no import-outside-toplevel)
- [ ] Code formatted according to project standards
- [ ] New tests added for new functionality
- [ ] Edge cases and error conditions tested
- [ ] No commented-out code or tests
- [ ] Pre-commit hooks pass without warnings

## Final Self-Check Before Committing

- [ ] Test suite passes completely
- [ ] Pylint/ESLint shows 10/10 or no violations
- [ ] Mypy/TypeScript shows zero errors
- [ ] Pre-commit hooks pass
- [ ] All imports at module top level
- [ ] Type annotations complete and accurate
- [ ] Test names are descriptive
- [ ] Tests verify behavior, not implementation
- [ ] No flaky or slow tests introduced
- [ ] Edge cases covered

**CRITICAL**: Never commit code with failing tests, lint violations, or type errors. Fix all issues before committing.
