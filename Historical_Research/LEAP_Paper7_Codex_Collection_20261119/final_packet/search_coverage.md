# Paper 7 read-only collection coverage

Result: NO_AUTHENTIC_AUTHORIZATIONS_FOUND in the inspected source scope. No authentic approval was exported and none could be associated with a source change. This extraction does not assign business or human reviewer decisions.

Repository alias: $REPO = AI-Powered_KPI_Extractor_Interactive_Bluebook_Generator at the --repo argument. HEAD: 9892e4477d87d32920bcd64918fd917d1f5fc796. Exact relative directories are in search/directories.txt. Git worktrees and refs are in search/git_worktrees.txt and search/git_refs.txt. No attached worktrees were returned by the desktop app. $HOME/.codex/worktrees did not exist. No remote system was queried.

## Working tree search

Included hidden, untracked and ignored files through os.walk, without following symlinks. Pruned directory names: ['.git', '.idea', '.pytest_cache', '.venv', '__pycache__', '_build', 'node_modules', 'venv']. Read extensions: ['.csv', '.json', '.jsonl', '.log', '.md', '.rst', '.sql', '.tsv', '.txt', '.yaml', '.yml']. Credential files are excluded. Files over 64 MiB are listed in exclusions. 14855 files read; 295503 matching lines. Every read content hash is in search/file_inventory.csv; expressions and exact line locators are in search/text_hits.csv. Expression: `approv(?:al|ed|er)?|deferr(?:al|ed)?|sign[ _-]?off|revok|revocat|exception|authoriz|signature`. JSON objects with authority field names are inventoried in structured_candidates.csv. A field-name hit is not an authentic approval. No source payloads, actor identities, session content, or corporate database row contents are exported.

## Ledgers and Git

215 working-tree or historical ledger path/blob observations. Working-tree override/workflow copies contain no records. Historical docs/overrides.json contains three descriptive text overrides without recorded approval metadata; fields and source blob hashes are in unsigned_override_texts.csv. Commands: `git log --all --format=%H -- <ledger paths>` and `git rev-list --objects --all -- <ledger paths>`, followed by `git cat-file blob <object>`. Ledger paths: ['docs/overrides.json', 'docs/governance_overrides.json', 'kb/overrides.json', 'bluebook_generator/kb/overrides.json', 'docs/review_workflow.json']. Exact revisions are in ledger_revisions.txt. Branch merge metadata is not counted as business authorization. No new PR reviews were fetched.

## SQLite

2 databases discovered. All table names, column names, exact SELECT queries, row counts and canonical row-set checksums are in search/sqlite_tables.csv. Connections use URI mode=ro, PRAGMA query_only=ON and an explicit read transaction. Each column was searched using the same expression; matching row ordinals, field names and row hashes are in sqlite_hits.csv. Context session/event state is software workflow evidence, not a supplied human authorization instrument. No database contents were exported.

## Archives and strata

All top-level Downloads Paper 7 ZIPs and nested ZIPs to depth 3 were inventoried (members up to 100 MiB for nested traversal). Exact archive/member locators are in archive_inventory.csv. The Sponsor supplied the local path LEAP_Paper7_Real_Revision_Authority_Gate_20261119.zip after the initial filename search. All input manifest members and all 18 before/after source hashes were verified. Exact input/archive checks and local Git byte comparisons are in verification/. Nine original historical transitions are imported without technical matcher predictions. The 24 constructed pilot case records are copied to constructed_pilot/recorded_case_inventory.csv with original row locators and recorded outputs; no cases are regenerated. Historical source finding outputs remain UNKNOWN where not supplied. Recorded Python behavior checks are copied separately to recorded_source_behavior.json and are not treated as business authorization outcomes.

## Coverage limits

Media filenames matching authority terms are inventoried but not visually interpreted; see media_inventory.csv. General binary archives other than the inventoried Paper 7 ZIPs were not unpacked. Excluded paths and parse/read errors are explicit in exclusions.csv and errors.csv. Git unreachable objects, external private systems, and human reviewers were not accessed. The finding is confined to inspected records, not all possible stores. No authentic authorization should be inferred from keyword hits, test fixtures, generated receipts, or code merge history.

## Reproduction and integrity

Optional --scan-cache reuses a completed file inventory from another collection directory while re-reading SQLite and Git; omit it for a fresh full scan.

Run `python -B extract_readonly.py --repo /path/to/repository --output /new/outside/repository/directory`. Repeat --archive for additional Paper 7 ZIPs. The script refuses an existing output directory and writes outside the repository only. Source code and runtime were not executed. Evidence hashes cover packet files; SHA256SUMS includes all files except itself. ZIP SHA-256 is supplied separately. Original source hashes and redacted export hashes are separately retained. No signed/manual reviewer decisions have been received. A human authorization study cannot be completed from code history alone.
