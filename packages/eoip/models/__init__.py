"""Local model abstraction layer and model governance (§49).

The package-level exports are resolved lazily so provider-only imports do not
eagerly import governance, agents, and retrieval back into each other.
"""

_EXPORTS = {
    "EvaluationDataset": "eoip.models.governance",
    "Feature": "eoip.models.governance",
    "FeatureDisabled": "eoip.models.governance",
    "FeatureDisabledReason": "eoip.models.governance",
    "GovernancePolicy": "eoip.models.governance",
    "HallucinationIncident": "eoip.models.governance",
    "HallucinationIncidentLog": "eoip.models.governance",
    "KillSwitch": "eoip.models.governance",
    "LocalModelProvider": "eoip.models.provider",
    "ModelEntry": "eoip.models.governance",
    "ModelHealth": "eoip.models.governance",
    "ModelOutput": "eoip.models.governance",
    "ModelRegistry": "eoip.models.governance",
    "ModelResponse": "eoip.models.provider",
    "OutputClass": "eoip.models.governance",
    "PolicyVerdict": "eoip.models.governance",
    "PromptTemplate": "eoip.models.governance",
    "PromptTemplateRegistry": "eoip.models.governance",
    "classify_model_output": "eoip.models.governance",
    "hash_template": "eoip.models.governance",
}

__all__ = sorted(_EXPORTS)


def __getattr__(name: str):
    if name not in _EXPORTS:
        raise AttributeError(f"module 'eoip.models' has no attribute {name!r}")
    from importlib import import_module

    value = getattr(import_module(_EXPORTS[name]), name)
    globals()[name] = value
    return value
