"""Evaluate expected log-source freshness against an explicit reference time."""

from runtime import cli, instant, integer, report, rows, text, unique, utc


def analyze(data):
    as_of = instant(data.get("as_of"), "as_of")
    scope = text(data.get("scope"), "scope")
    sources = rows(data.get("sources"), "sources")
    unique(sources)
    findings = []
    for source in sources:
        owner = text(source.get("owner"), "source.owner")
        limit = integer(source.get("max_silence_seconds"), "max_silence_seconds", 1)
        last_seen = source.get("last_seen")
        age = None
        if last_seen is None:
            health = "unknown"
        else:
            parsed = instant(last_seen, "source.last_seen")
            age = (as_of - parsed).total_seconds()
            health = (
                "future_timestamp" if age < 0 else "stale" if age > limit else "fresh"
            )
            last_seen = utc(parsed)
        maintenance = source.get("maintenance_until")
        active_maintenance = (
            maintenance is not None
            and instant(maintenance, "maintenance_until") > as_of
        )
        findings.append(
            {
                "source_id": source["id"],
                "owner": owner,
                "freshness": health,
                "status": "maintenance" if active_maintenance else health,
                "last_seen": last_seen,
                "age_seconds": age,
                "max_silence_seconds": limit,
                "maintenance_until": utc(instant(maintenance, "maintenance_until"))
                if maintenance
                else None,
            }
        )
    return report(
        "Telemetry Health Agent",
        {
            "scope": scope,
            "as_of": utc(as_of),
            "expected_sources": len(sources),
            "needs_review": sum(
                f["status"] not in ("fresh", "maintenance") for f in findings
            ),
            "in_maintenance": sum(f["status"] == "maintenance" for f in findings),
        },
        findings,
        [
            "A recent event establishes freshness only, not completeness, parsing quality or correct event volume.",
            "Missing last_seen is unknown, not evidence of zero activity. Future timestamps require clock/source review.",
            "Expected sources, thresholds and maintenance windows are caller supplied; quiet sources need context-specific thresholds.",
            "No SIEM query, notification, suppression or configuration change is performed.",
        ],
        [
            "Check collection credentials, delivery errors, parsing and expected source activity for stale or unknown sources.",
            "Check clocks and ingestion-time semantics for future timestamps.",
            "Verify recovery with fresh events and volume checks before marking a pipeline healthy.",
        ],
    )


if __name__ == "__main__":
    cli(analyze, __doc__)
