# Upstream Sync Ledger

Tracks synchronization from upstream [`yihong0618/running_page`](https://github.com/yihong0618/running_page) into `jimrory/running_page`.

- **Current upstream baseline**: `1730095` (2026-11-19)
- **Safety rules & baseline reference**: see `docs/upgrade-2026-10.md`.

## Sync History

| Date | Upstream Baseline | Applied | Skipped | Notes |
|---|---|---|---|---|
| 2026-10-28 | `3bec720` (2026-10-26) | Running Page 3.0 upgrade (PR #1) | — | Initial 3.0 upgrade by Codex; see `docs/upgrade-2026-10.md` |
| 2026-11-21 | `1730095` (2026-11-19) | `#1161` (`cc1e3b1`), `#1162` (`7b27fa3`), `#1167` (`15c553e`, `be82382`) | `#1163` (`06afe09`, `df43d9e`) | Python-only fixes (extension-only GPX, `default_timezone()`, Ruff cleanup); skipped unrelated runner domain update |
