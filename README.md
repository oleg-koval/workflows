# workflows

> Reusable GitHub Actions workflows for [@oleg-koval](https://github.com/oleg-koval) repositories.

[![ci](https://github.com/oleg-koval/workflows/actions/workflows/ci.yml/badge.svg)](https://github.com/oleg-koval/workflows/actions)

---

## Workflows

### Contribution governance

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| [prevent-unknown-contributors](.github/workflows/prevent-unknown-contributors.yml) | `pull_request_target: opened` | Closes PRs from first-time contributors, adds `needs-issue` label, posts friendly message |

### Security

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| [secret-scan-gitleaks](.github/workflows/secret-scan-gitleaks.yml) | `push`, `pull_request` | Gitleaks scan with SHA-pinned checkout + checksum verification |
| [scorecard](.github/workflows/scorecard.yml) | weekly, `push: main` | OpenSSF Scorecard supply-chain security — results in Security tab |

### Quality gates

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| [commitlint](.github/workflows/commitlint.yml) | `pull_request` | Enforce conventional commit messages on all PR commits |
| [semantic-pr-title](.github/workflows/semantic-pr-title.yml) | `pull_request_target` | Enforce semantic/conventional PR title format |
| [anti-slop](.github/workflows/anti-slop.yml) | `pull_request` | Block AI-generated filler phrases in PR diffs |
| [docs-index-keeper](.github/workflows/docs-index-keeper.yml) | `push`/`pull_request` to `docs/**` | Require docs/README.md index to be up to date |

### Performance

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| [lighthouse-performance](.github/workflows/lighthouse-performance.yml) | `push`, `pull_request` | Non-blocking Lighthouse CI — annotates but never blocks merge |

### Infrastructure & Automation

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| [supabase-keepalive](.github/workflows/supabase-keepalive.yml) | every 3 days | Ping Supabase endpoint to prevent free-tier project pause |
| [automerge-github-action](.github/workflows/automerge-github-action.yml) | `pull_request_target`, `check_suite`, `pull_request_review` | Auto-merge PRs from bots & maintainers using `oleg-koval/pr-automerge-github-action` |
| [dependabot-auto-merge](.github/workflows/dependabot-auto-merge.yml) | `pull_request_target` | Auto-merge Dependabot npm **patch-only** bumps after CI (narrower alternative) |

### Maintenance

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| [backfill-releases](.github/workflows/backfill-releases.yml) | `workflow_dispatch`, after Release | Create missing GitHub releases from existing git tags |

---

## Usage

Copy the workflow file into your repo's `.github/workflows/` directory:

```bash
# Example: add secret scanning
curl -O https://raw.githubusercontent.com/oleg-koval/workflows/main/.github/workflows/secret-scan-gitleaks.yml
mv secret-scan-gitleaks.yml .github/workflows/
```

No secrets or external dependencies beyond what each workflow documents. Secrets required per workflow:

| Workflow | Required secrets/vars |
|----------|-----------------------|
| `supabase-keepalive` | `SUPABASE_KEEPALIVE_URL` (secret) |
| `lighthouse-performance` | `LHCI_GITHUB_APP_TOKEN` (optional) |
| `backfill-releases` | `BACKFILL_MIN_TAG` (var, optional) |
| `secret-scan-gitleaks` | `INTERNAL_REF_PATTERN` (var, optional) |
| `automerge-github-action` | none (uses GITHUB_TOKEN) |

---

## Rules

All workflows follow [RULES.md](https://github.com/oleg-koval/starters/blob/main/RULES.md):
- Single responsibility per workflow
- Explicit `permissions:` block — no implicit write-all
- Self-contained — no custom Actions from untrusted sources (exception: pinned SHA)
- SHA-pinned third-party Actions where security matters (see `secret-scan-gitleaks`)

---

## Contributing

Open an issue first. PRs without a linked issue are labelled `needs-issue` and closed automatically by [prevent-unknown-contributors](.github/workflows/prevent-unknown-contributors.yml).

---

*Part of [oleg-koval/starters](https://github.com/oleg-koval/starters)*
