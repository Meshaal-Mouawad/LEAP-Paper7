def _definition_override_candidates(kpi: dict) -> list[str]:
    candidates = [
        str(kpi.get("name") or "").strip(),
        str(kpi.get("function_name") or "").strip(),
        str(kpi.get("source_file_display") or "").strip(),
        Path(str(kpi.get("file_path") or "")).stem,
    ]
    return [c for c in candidates if c]

def _apply_definition_override(kpi: dict, details: dict, overrides: dict) -> dict:
    if not overrides:
        return details
    override = None
    for candidate in _definition_override_candidates(kpi):
        if candidate in overrides:
            override = overrides[candidate]
            break
    if not override:
        return details
    override_signature = str(override.get("file_signature") or "").strip()
    current_signature = str(kpi.get("source_file_signature") or "").strip()
    if override_signature and override_signature != current_signature:
        return details
    fields = override.get("fields", {}) if isinstance(override, dict) else {}
    if not isinstance(fields, dict):
        return details
    updated = dict(details or {})
    for key in DEFINITION_OVERRIDE_FIELDS:
        value = fields.get(key)
        if value is not None and str(value).strip():
            updated[key] = value
    updated["_override_status"] = override.get("status") or "APPROVED_BY_BUSINESS"
    updated["_override_source"] = override.get("source") or "manual override ledger"
    return updated
