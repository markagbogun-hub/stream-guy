# RadioCastOS 1.89.1 — Deployment Package Hardening & Playout Tracking Fixes

## Fixed
- Deployment hash verification could be bypassed with a backslash-named archive member; verified packages now refuse unexpected, unsafe or ambiguous member names.
- Package inspection no longer loads whole members into memory; sizes are enforced while streaming.
- Import is all-or-nothing: validation and staging complete before any station file is replaced.
- Exports and imports redact the operator PIN hash, `*_password/_secret/_token/_api_key` fields and credentials embedded in URLs.
- Scheduled playout: repeat airings of one file are tracked separately, path-only as-run rows cannot confirm items that never started, and an item that exhausts its retries no longer blocks the queue.
- The Import dialog shows verified / unverified status before you confirm.

## Behaviour change
- Items that fail every retry are now removed from the canonical queue and written to the audit log. `ScheduledPlayoutController(skip_exhausted=False)` restores the previous behaviour.
- Verified packages containing members outside the declared list (or with backslash names) are now refused; packages exported by 1.89.0 itself are unaffected.

## Still required on the station computer
Windows installer build, GUI behaviour on a real Windows desktop (this release's dialog change was import-checked only), audio devices, encoder delivery, as-run reconciliation and a supervised 24-hour soak test. The package manifest is still unsigned.
