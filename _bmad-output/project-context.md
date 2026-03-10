---
project_name: dont-stop-til-you-get-enough
user_name: Boss
date: '2026-03-10T20:57:00.000Z'
sections_completed:
  - technology_stack
  - language_rules
  - code_quality
  - testing_rules
  - workflow_rules
  - critical_rules
status: complete
rule_count: 18
optimized_for_llm: true
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

- **Python**: >=3.13 (use patterns compatible with 3.11+)
- **Package Manager**: uv
- **Testing**: pytest
- **Linting/Formatting**: ruff
- **Project Layout**: src/ (package in src/, tests alongside)

## Critical Implementation Rules

### Language-Specific Rules

- Use type hints for all function signatures
- Follow PEP 8 style guide
- Use f-strings for string formatting
- Avoid walrus operator (:=) for clarity
- Use dataclasses for simple data structures

### Code Quality & Style Rules

- Run `ruff check .` before commits
- Run `ruff format .` for formatting
- Maximum line length: 88 (ruff default)
- Use absolute imports within package

### Testing Rules

- Tests in `tests/` directory at project root
- Test files: `test_*.py` pattern
- Use pytest fixtures for shared setup
- Aim for >80% code coverage

### Development Workflow Rules

- **Branch naming**: `feature/`, `bugfix/`, `hotfix/` prefixes
- **Commit messages**: Conventional commits (`feat:`, `fix:`, `docs:`)
- **PR requirements**: At least one review, tests passing

### Critical Don't-Miss Rules

**Anti-Patterns to Avoid:**
- Don't commit debug print statements
- Don't leave TODO comments without issue references
- Don't hardcode secrets (use environment variables)
- Don't skip error handling

**Security Rules:**
- Store secrets in .env files, never commit them
- Use environment variables for configuration

---

## Usage Guidelines

**For AI Agents:**
- Read this file before implementing any code
- Follow ALL rules exactly as documented
- When in doubt, prefer the more restrictive option
- Update this file if new patterns emerge

**For Humans:**
- Keep this file lean and focused on agent needs
- Update when technology stack changes
- Review quarterly for outdated rules
- Remove rules that become obvious over time

Last Updated: 2026-03-10
