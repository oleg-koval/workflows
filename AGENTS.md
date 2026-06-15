# AGENTS.md

Inherits all rules from [oleg-koval/starters RULES.md](https://github.com/oleg-koval/starters/blob/main/RULES.md).

## Repo-specific rules

- Workflow files live in `.github/workflows/`
- Every workflow must declare `permissions:` explicitly — no implicit write-all
- Use `pull_request_target` (not `pull_request`) for workflows that need write access to PRs from forks
- Validate YAML before pushing: `python3 -c "import yaml; yaml.safe_load(open('file.yml'))"`
- No third-party Actions beyond `actions/*` and `github/codeql-action` without documented reason
