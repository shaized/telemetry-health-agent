# Telemetry Health Agent

## Summary

- **scope:** Fictional lab source inventory
- **as of:** 2026-01-15T12:00:00Z
- **expected sources:** 3
- **needs review:** 2
- **in maintenance:** 0

## Findings

### Finding 1

- **source id:** identity
- **owner:** Identity team
- **freshness:** fresh
- **status:** fresh
- **last seen:** 2026-01-15T11:58:00Z
- **age seconds:** 120\.0
- **max silence seconds:** 900
- **maintenance until:** null

### Finding 2

- **source id:** endpoint
- **owner:** Endpoint team
- **freshness:** stale
- **status:** stale
- **last seen:** 2026-01-15T10:30:00Z
- **age seconds:** 5400\.0
- **max silence seconds:** 900
- **maintenance until:** null

### Finding 3

- **source id:** audit
- **owner:** Platform team
- **freshness:** unknown
- **status:** unknown
- **last seen:** null
- **age seconds:** null
- **max silence seconds:** 3600
- **maintenance until:** null


## Limitations

- A recent event establishes freshness only, not completeness, parsing quality or correct event volume\.
- Missing last\_seen is unknown, not evidence of zero activity\. Future timestamps require clock/source review\.
- Expected sources, thresholds and maintenance windows are caller supplied; quiet sources need context-specific thresholds\.
- No SIEM query, notification, suppression or configuration change is performed\.

## Next Steps

- Check collection credentials, delivery errors, parsing and expected source activity for stale or unknown sources\.
- Check clocks and ingestion-time semantics for future timestamps\.
- Verify recovery with fresh events and volume checks before marking a pipeline healthy\.
