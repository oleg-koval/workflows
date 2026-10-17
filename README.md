# workflows

> Reusable GitHub Actions workflows for [@oleg-koval](https://github.com/oleg-koval) repositories.

See [CONSUMING.md](CONSUMING.md) for the versioning and adoption contract.

[![ci](https://github.com/oleg-koval/workflows/actions/workflows/ci.yml/badge.svg)](https://github.com/oleg-koval/workflows/actions)
[![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/oleg-koval/workflows?utm_source=oss&utm_medium=github&utm_campaign=oleg-koval%2Fworkflows&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)](https://coderabbit.ai)

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

### Code review

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| [agent-hygiene-review](.github/workflows/agent-hygiene-review.yml) | `pull_request` | Runs `agent-hygiene-linter` against the PR branch and surfaces repo hygiene issues in the job summary |

### Performance

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| [lighthouse-performance](.github/workflows/lighthouse-performance.yml) | `push`, `pull_request` | Non-blocking Lighthouse CI — annotates but never blocks merge |

### Infrastructure & Automation

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| [supabase-keepalive](.github/workflows/supabase-keepalive.yml) | every 3 days | Ping Supabase endpoint to prevent free-tier project pause |
| [automerge-github-action](.github/workflows/automerge-github-action.yml) | PR, review, comment, schedule, manual dispatch | Auto-merge PRs from bots & maintainers using the review-thread-safe [`oleg-koval/pr-automerge-github-action`](https://github.com/oleg-koval/pr-automerge-github-action) |
| [dependabot-auto-merge](.github/workflows/dependabot-auto-merge.yml) | `pull_request_target` | Auto-merge Dependabot npm **patch-only** bumps after CI (narrower, safer alternative) |

### Maintenance

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| [backfill-releases](.github/workflows/backfill-releases.yml) | `workflow_dispatch`, after Release | Create missing GitHub releases from existing git tags |

---

## Usage

### Reusable workflows (recommended)

8 of the 14 workflows support `workflow_call` — call them directly from your repo without copying files. Pin the catalog to an immutable commit SHA; do not use `@main` in production:

```yaml
# .github/workflows/ci.yml in your repo
jobs:
  secret-scan:
    uses: oleg-koval/workflows/.github/workflows/secret-scan-gitleaks.yml@f4ad5f2aa325a7fd61b2f7c2fb096e77570b963b # workflows v1

  commitlint:
    uses: oleg-koval/workflows/.github/workflows/commitlint.yml@f4ad5f2aa325a7fd61b2f7c2fb096e77570b963b # workflows v1
    with:
      base-sha: ${{ github.event.pull_request.base.sha }}
      head-sha: ${{ github.event.pull_request.head.sha }}

  agent-hygiene:
    uses: oleg-koval/workflows/.github/workflows/agent-hygiene-review.yml@f4ad5f2aa325a7fd61b2f7c2fb096e77570b963b # workflows v1
    with:
      min-score: 80

  lighthouse:
    uses: oleg-koval/workflows/.github/workflows/lighthouse-performance.yml@f4ad5f2aa325a7fd61b2f7c2fb096e77570b963b # workflows v1
    secrets:
      LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}

  keepalive:
    uses: oleg-koval/workflows/.github/workflows/supabase-keepalive.yml@f4ad5f2aa325a7fd61b2f7c2fb096e77570b963b # workflows v1
    secrets:
      SUPABASE_KEEPALIVE_URL: ${{ secrets.SUPABASE_KEEPALIVE_URL }}

  backfill:
    uses: oleg-koval/workflows/.github/workflows/backfill-releases.yml@f4ad5f2aa325a7fd61b2f7c2fb096e77570b963b # workflows v1
    with:
      min-release-tag: v1.0.0

  scorecard:
    uses: oleg-koval/workflows/.github/workflows/scorecard.yml@f4ad5f2aa325a7fd61b2f7c2fb096e77570b963b # workflows v1
    with:
      publish-results: false

  docs-check:
    uses: oleg-koval/workflows/.github/workflows/docs-index-keeper.yml@f4ad5f2aa325a7fd61b2f7c2fb096e77570b963b # workflows v1
```

Or pass all secrets at once with `secrets: inherit`:

```yaml
jobs:
  secret-scan:
    uses: oleg-koval/workflows/.github/workflows/secret-scan-gitleaks.yml@f4ad5f2aa325a7fd61b2f7c2fb096e77570b963b # workflows v1
    secrets: inherit
```

**Workflows NOT usable via `workflow_call`:**
- `anti-slop` — requires PR diff context not available outside `pull_request` events
- `semantic-pr-title` — requires PR title not available in `workflow_call` context
- `dependabot-auto-merge` — inspects PR metadata not available outside `pull_request_target`
- `prevent-unknown-contributors` — inspects PR author/status not available outside `pull_request_target`

### Copy-paste (alternative)

Copy the workflow file into your repo's `.github/workflows/` directory:

```bash
# Example: add secret scanning from the approved catalog revision
curl -o secret-scan-gitleaks.yml https://raw.githubusercontent.com/oleg-koval/workflows/f4ad5f2aa325a7fd61b2f7c2fb096e77570b963b/.github/workflows/secret-scan-gitleaks.yml
mv secret-scan-gitleaks.yml .github/workflows/
```

### Callable workflows: inputs & secrets

| Workflow | Inputs | Secrets | Notes |
|----------|--------|---------|-------|
| `agent-hygiene-review` | `min-score` (number, default `75`) | — | Runs agent-hygiene-linter logic against the caller repo; use the published-action migration in [PR #7](https://github.com/oleg-koval/workflows/pull/7) when adopting |
| `commitlint` | `base-sha`, `head-sha` (strings, optional) | — | When using outside PR context, must pass both SHAs |
| `secret-scan-gitleaks` | `internal-ref-pattern` (string, optional) | — | |
| `backfill-releases` | `min-release-tag` (string, optional) | — | Falls back to `vars.BACKFILL_MIN_TAG`, then `v0.0.0` |
| `lighthouse-performance` | — | `LHCI_GITHUB_APP_TOKEN` (optional) | |
| `supabase-keepalive` | — | `SUPABASE_KEEPALIVE_URL` (required) | |
| `scorecard` | `publish-results` (bool, default `false`) | — | Requires Code Scanning enabled to publish SARIF |
| `automerge-github-action` | none (uses GITHUB_TOKEN) |
| `docs-index-keeper` | — | — | |

For the full distribution contract and the boundary between reusable and event-bound workflows, see [CONSUMING.md](CONSUMING.md).

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
