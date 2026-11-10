# Input and output contract

## Input

The root requires as_of, scope and sources. Each source needs unique id, owner, positive integer max_silence_seconds and last_seen (offset-aware timestamp or null). Optional maintenance_until is an offset-aware timestamp. A source is stale only when its age is strictly greater than the limit; negative age is future_timestamp. Active maintenance changes status but preserves underlying freshness. Expired maintenance does not suppress the result. Null last_seen is unknown.

See [example.json](example.json) for a complete fictional input. All demo identities, indicators, events, products and reputation providers are synthetic. Documentation IPs and example domains are not threat intelligence.

Input must be a UTF-8 JSON object no larger than 2 MiB. Duplicate JSON keys, malformed required fields, ambiguous timestamps and conflicting identifiers are rejected. Timestamps require an explicit UTC offset. Small local snapshots are the intended workload; there is no streaming, database or production connector in this version.

## Output

`python3 agent.py INPUT.json` emits Markdown. Add `--format json` for structured output. The JSON envelope contains schema_version, agent, summary, findings, limitations and next_steps. The tool writes to standard output and does not modify the source input. Input errors return exit code 2; a valid assessment returns 0 even when findings are present.

JSON preserves evidence text. Markdown renders evidence as literal escaped text, so input cannot inject links, headings or HTML into the report. Every result preserves substantive limitations.

## Example interpretation

One fresh source, one stale source and one source with unknown freshness. Freshness is explicitly separated from full pipeline health.

Thresholds should reflect each source's expected behavior, maintenance schedule and timestamp semantics. No particular SIEM is assumed.
