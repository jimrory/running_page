---
name: upstream-sync
description: >-
  Sync updates from upstream yihong0618/running_page into jimrory/running_page
  safely while preserving historical Nike/Strava data and personal customizations.
---

# Upstream Sync Guide (`yihong0618/running_page` -> `jimrory/running_page`)

Use this skill whenever the user asks to check, review, or sync updates from `yihong0618/running_page` into `jimrory/running_page`.

## 1. Check Baseline & Fetch Upstream

1. Read `docs/upstream-sync.md` to get the last recorded upstream baseline commit SHA and date.
2. Ensure remotes and `master` are up to date:
   ```bash
   git fetch origin
   git fetch upstream
   ```
3. List new upstream commits since the recorded baseline:
   ```bash
   git log --oneline --no-merges <baseline_sha>..upstream/master
   ```
4. If there are new commits, inspect each commit (`git show --stat <sha>` or `git show <sha>`) and group them by upstream PR.

## 2. Commit Triage Rules

- **Skip unconditionally**:
  - Other users' personal README runner links / homepage domain updates.
  - Upstream personal data (`run_page/data.db`, `src/static/activities.json`, `assets/`, `GPX_OUT/`, `FIT_OUT/`, `TCX_OUT/`, `PNG_OUT/`, `Workouts/`).
  - Upstream personal `config.yml`, `.github/workflows/*` changes that conflict with our deployment/sync setup, or `public/` personal assets.
- **Evaluate carefully**:
  - Changes to `run_page/` Python syncers, database schema, or exporter (`generator/`).
  - Frontend (`src/`) changes that might touch themes, map renderer, or footer/metadata.
- **Usually safe to sync**:
  - Bug fixes in `run_page/gpxtrackposter/` or `run_page/generator/`.
  - Linter/type/test fixes and dependency updates (verify with local checks).

## 3. Non-Negotiable Preservation Checklist (from `docs/upgrade-2026-10.md`)

Never break or overwrite any of the following personal customizations:

1. **Historical Data Protection**:
   - **Never** wipe or re-fetch SQLite (`run_page/data.db`) from Nike or Strava; Nike historical records cannot be re-fetched online.
   - Preserve the Strava sync history-ID guard (`test_check_history.py` and workflow checks) that blocks publishing if any existing activity ID disappears or the DB is empty/corrupt.
   - Preserve existing columns and historical `NULL` values (e.g., `subtype`, `elevation_gain`); never fabricate historical data.
2. **Deployment & CI/CD**:
   - Keep `vercel.json` (Vite, `pnpm run build`, `dist`, SPA rewrites) and `pnpm 8.9.0` compatibility.
   - Keep GitHub Pages disabled; site is deployed on Vercel.
   - Keep daily UTC 00:00 (Beijing 08:00) Strava incremental sync and existing Secrets references (`STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET`, `STRAVA_CLIENT_REFRESH_TOKEN`).
3. **Frontend & Personal Metadata**:
   - Keep MapLibre + CARTO fallback when no Mapbox Token is provided (while preserving Mapbox renderer when a token is explicitly provided).
   - Keep personal domain, site title, avatar, favicon, and personal links.
   - Keep Month of Life generation disabled (no unknown birthday).
   - Keep Dashboard footer without the `3.0` version number.

## 4. Branch, Sync & PR Workflow

1. Create a feature branch from the latest `origin/master`:
   ```bash
   git checkout master
   git pull --ff-only origin master
   git checkout -b sync/upstream-YYYY-MM
   ```
2. Cherry-pick (or selectively merge) the approved upstream commits in chronological order.
   - If a commit touches `run_page/data.db`, `src/static/activities.json`, or personal configs, stop and resolve without overwriting personal data.
   - If upstream introduces new SQLite columns or exporter changes, migrate the latest `origin/master` DB cleanly and verify every existing DB record and exported JSON record against `origin/master`.
3. **Verify before pushing**:
   - Confirm `git diff --stat origin/master..HEAD` shows `run_page/data.db` and `src/static/activities.json` are untouched (unless an intentional, verified migration was performed).
   - Run Python tests (`pytest` / `test_check_history.py`, `test_generator.py`, etc.) and `ruff check` on Python changes.
   - If any frontend (`src/`, `package.json`, `vite.config.ts`, `tsconfig.json`) files changed, run `pnpm run build`, TypeScript check, ESLint, and Prettier.
4. Update `docs/upstream-sync.md` with the new upstream baseline SHA, date, applied PRs/commits, and skipped PRs/commits, and commit it.
5. Push the branch to `origin` and provide the GitHub PR/compare link so the user can verify **Vercel Preview** before merging.
6. **Before merging the PR**: Always check if daily Strava sync added new commits to `origin/master` while the PR was open; if so, rebase/re-verify against the latest `master` so no new runs are overwritten.
