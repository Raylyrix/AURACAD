"""Shared NativeIauracad availability helpers."""

import importlib.util

import AuraCAD

translate = AuraCAD.Qt.translate

_iauracadopenshell_state = {"available": None, "reported_missing": False}


def invalidate_iauracadopenshell_cache():
    """Clears the cached iauracadopenshell availability state."""

    _iauracadopenshell_state["available"] = None
    _iauracadopenshell_state["reported_missing"] = False


def has_iauracadopenshell(report=False):
    """Returns True when iauracadopenshell is importable in this runtime."""

    if _iauracadopenshell_state["available"] is None:
        _iauracadopenshell_state["available"] = importlib.util.find_spec("iauracadopenshell") is not None

    if report and not _iauracadopenshell_state["available"]:
        report_missing_iauracadopenshell()

    return _iauracadopenshell_state["available"]


def report_missing_iauracadopenshell():
    """Reports the missing iauracadopenshell dependency once per runtime."""

    if _iauracadopenshell_state["reported_missing"]:
        return

    AuraCAD.Console.PrintError(
        translate(
            "BIM",
            "IauracadOpenShell was not found on this system. Iauracad support is disabled",
        )
        + "\n"
    )
    _iauracadopenshell_state["reported_missing"] = True
