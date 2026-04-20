"""Managed PolicyEngine runtime helpers for reproducible analysis runs."""

from __future__ import annotations


def managed_us_microsimulation(
    *,
    dataset: str | None = None,
    allow_unmanaged: bool = False,
    **kwargs,
):
    """Construct a US Microsimulation pinned to the current PolicyEngine bundle."""

    from policyengine.tax_benefit_models.us import managed_microsimulation

    return managed_microsimulation(
        dataset=dataset,
        allow_unmanaged=allow_unmanaged,
        **kwargs,
    )


def managed_uk_microsimulation(
    *,
    dataset: str | None = None,
    allow_unmanaged: bool = False,
    **kwargs,
):
    """Construct a UK Microsimulation pinned to the current PolicyEngine bundle.

    Falls back to loading `policyengine_uk.Microsimulation` directly when
    the managed runtime cannot be imported (e.g. the bundled
    policyengine-us version and HuggingFace data release manifest are out
    of sync locally). The direct path still uses the HF-hosted enhanced
    FRS dataset and HUGGING_FACE_TOKEN for authentication.
    """
    try:
        from policyengine.tax_benefit_models.uk import managed_microsimulation

        return managed_microsimulation(
            dataset=dataset,
            allow_unmanaged=allow_unmanaged,
            **kwargs,
        )
    except Exception:
        from policyengine_uk import Microsimulation

        return Microsimulation(
            dataset=dataset
            or "hf://policyengine/policyengine-uk-data/enhanced_frs_2023_24.h5"
        )


def policyengine_bundle(sim) -> dict:
    """Return a detached copy of policyengine.py release metadata when present."""

    bundle = getattr(sim, "policyengine_bundle", None)
    if not isinstance(bundle, dict):
        return {}
    return dict(bundle)
