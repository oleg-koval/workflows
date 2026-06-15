# workflows

> Reusable GitHub Actions workflows for [@oleg-koval](https://github.com/oleg-koval) repositories.

[![ci](https://github.com/oleg-koval/workflows/actions/workflows/ci.yml/badge.svg)](https://github.com/oleg-koval/workflows/actions)

---

## Workflows

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| [prevent-unknown-contributors](.github/workflows/prevent-unknown-contributors.yml) | `pull_request_target: opened` | Closes PRs from first-time contributors with a friendly message pointing them to open an issue first |

---

## Usage

Copy the workflow file into your repo's `.github/workflows/` directory:

```bash
curl -O https://raw.githubusercontent.com/oleg-koval/workflows/main/.github/workflows/prevent-unknown-contributors.yml
mv prevent-unknown-contributors.yml .github/workflows/
```

No secrets or external dependencies required. The workflow uses `GITHUB_TOKEN` with minimal permissions.

---

## Rules

All workflows follow [RULES.md](https://github.com/oleg-koval/starters/blob/main/RULES.md) from [oleg-koval/starters](https://github.com/oleg-koval/starters):
- Single responsibility per workflow
- Minimal permissions (`permissions:` block required)
- Self-contained — no custom Actions from untrusted sources

---

## Contributing

Open an issue first. PRs without a linked issue are closed automatically by [prevent-unknown-contributors](.github/workflows/prevent-unknown-contributors.yml).

---

*Part of [oleg-koval/starters](https://github.com/oleg-koval/starters)*
