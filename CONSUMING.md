# Consuming shared workflows

`oleg-koval/workflows` is the policy library for repository-wide checks. Consumer repositories keep their product, deployment, NAS, and data-pipeline workflows locally and opt into shared checks explicitly.

## Versioning rule

Pin every production use to an immutable commit SHA. The repository has no stable release tag yet; until a release is published, use the merge commit of the approved `workflows` PR and leave a version comment beside it.

```yaml
jobs:
  secret-scan:
    uses: oleg-koval/workflows/.github/workflows/secret-scan-gitleaks.yml@<workflows-sha> # workflows v1
```

Do not use `@main` in a consumer repository. A release tag may be used for local experiments, but an exact SHA remains the production default.

## Reusable checks

Use `workflow_call` for checks that only need the caller repository and normal workflow inputs:

- `agent-hygiene-review`
- `backfill-releases`
- `commitlint`
- `docs-index-keeper`
- `lighthouse-performance`
- `scorecard`
- `secret-scan-gitleaks`
- `supabase-keepalive`

A consumer wrapper can combine these jobs:

```yaml
name: Shared repository quality

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  secret-scan:
    uses: oleg-koval/workflows/.github/workflows/secret-scan-gitleaks.yml@<workflows-sha> # workflows v1

  commitlint:
    uses: oleg-koval/workflows/.github/workflows/commitlint.yml@<workflows-sha> # workflows v1
    with:
      base-sha: ${{ github.event.pull_request.base.sha || github.event.before }}
      head-sha: ${{ github.event.pull_request.head.sha || github.sha }}

  scorecard:
    permissions:
      actions: read
      contents: read
      id-token: write
      security-events: write
    uses: oleg-koval/workflows/.github/workflows/scorecard.yml@<workflows-sha> # workflows v1
    with:
      publish-results: false
```

The exact job inputs and required secrets are documented in the root README. Keep the wrapper small: project-specific build and deployment jobs should remain in their existing workflows.

## Event-bound workflows

Some workflows depend on event payloads or elevated permissions that are not safely portable through `workflow_call`:

- `anti-slop`
- `automerge-github-action`
- `dependabot-auto-merge`
- `prevent-unknown-contributors`
- `semantic-pr-title`

Copy those files through a deliberate PR or a repository-local sync tool. Do not silently overwrite a project workflow with a shared template.

## Consumer update process

1. Select the shared checks the repository actually needs.
2. Pin all calls to one `workflows` SHA.
3. Add or update a small wrapper under `.github/workflows/`.
4. Leave project-specific workflows untouched.
5. Run the repository's real local checks.
6. Push one branch and open one PR.
7. Update the SHA only through a later dependency PR.

This makes workflow changes reviewable and lets repositories adopt the catalog at different speeds.
