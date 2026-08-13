from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Iterable


DERIVED_FLOW_FIELDS = (
    "ehr_lane",
    "ehr_lane_label",
    "outside_ehr",
    "outside_kind",
    "outside_kind_label",
)

LANE_INSIDE = "inside_ehr"
LANE_CROSSES = "crosses_ehr"
LANE_OUTSIDE = "outside_ehr"

LANE_LABELS = {
    LANE_INSIDE: "Stays in the EHR",
    LANE_CROSSES: "Leaves or enters the EHR",
    LANE_OUTSIDE: "Never touches the EHR",
}

KIND_EHR = "ehr"
KIND_AI = "ai"
KIND_EMAIL = "email"
KIND_FILES = "files"
KIND_IMAGING = "imaging"
KIND_MESSAGING = "messaging"
KIND_FAX = "fax"
KIND_PHONES = "phones"
KIND_BILLING = "billing"
KIND_PORTAL = "vendor_portal"
KIND_PEOPLE = "people_process"
KIND_OTHER = "other"

KIND_LABELS = {
    KIND_EHR: "EHR",
    KIND_AI: "AI tool",
    KIND_EMAIL: "Email",
    KIND_FILES: "Shared files / backup",
    KIND_IMAGING: "Imaging / export",
    KIND_MESSAGING: "Messaging / portal",
    KIND_FAX: "Fax",
    KIND_PHONES: "Phones / voicemail",
    KIND_BILLING: "Billing / claims",
    KIND_PORTAL: "Vendor portal / intake",
    KIND_PEOPLE: "People / paper / process",
    KIND_OTHER: "Other sidecar",
}

EHR_CATEGORIES = {"ehr", "emr"}
EHR_NAME_MARKERS = ("electronic health", "electronic medical", "ehr / emr")
EHR_NAME_TOKENS = {"ehr", "emr"}

CATEGORY_KIND = {
    "ehr": KIND_EHR,
    "emr": KIND_EHR,
    "ai workflow": KIND_AI,
    "ai drafting": KIND_AI,
    "ai documentation": KIND_AI,
    "email": KIND_EMAIL,
    "file storage": KIND_FILES,
    "backup": KIND_FILES,
    "imaging": KIND_IMAGING,
    "messaging": KIND_MESSAGING,
    "patient communications": KIND_MESSAGING,
    "patient portal": KIND_MESSAGING,
    "fax": KIND_FAX,
    "communications": KIND_PHONES,
    "billing": KIND_BILLING,
    "claims": KIND_BILLING,
    "intake": KIND_PORTAL,
    "scheduling": KIND_PORTAL,
    "lab": KIND_PORTAL,
    "prescribing": KIND_PORTAL,
    "telehealth": KIND_PORTAL,
}

KIND_MARKERS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (KIND_AI, ("chatbot", "chatgpt", "copilot", "scribe", "ai assistant", "ai tool", "ai draft")),
    (KIND_EMAIL, ("email", "inbox", "outlook", "gmail", "calendar")),
    (KIND_FILES, ("shared drive", "sharepoint", "google drive", "onedrive", "file storage", "usb", "thumb drive", "backup")),
    (KIND_IMAGING, ("imaging", "x-ray", "xray", "pacs", "dicom", "sensor")),
    (KIND_MESSAGING, ("texting", "sms", "secure message", "patient portal", "messaging")),
    (KIND_FAX, ("efax", "fax")),
    (KIND_PHONES, ("voicemail", "voip", "phone")),
    (KIND_BILLING, ("billing", "claims", "clearinghouse", "payer")),
    (KIND_PORTAL, ("intake form", "digital intake", "scheduling", "lab portal", "telehealth")),
    (KIND_PEOPLE, ("front desk", "provider", "specialist", "contractor", "staff", "patient", "conversation", "notes", "paper", "print")),
)

RISK_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


@dataclass(frozen=True)
class EndpointClass:
    label: str
    is_ehr: bool
    kind: str
    matched_system: str | None


@dataclass(frozen=True)
class FlowClass:
    lane: str
    kind: str
    source: EndpointClass
    destination: EndpointClass

    @property
    def outside_ehr(self) -> bool:
        return self.lane != LANE_INSIDE


def _normalize(value: object) -> str:
    return " ".join(str(value or "").casefold().split())


def _tokens(value: object) -> set[str]:
    return {token for token in "".join(char if char.isalnum() else " " for char in _normalize(value)).split() if token}


def _contains_marker(text: str, markers: Iterable[str]) -> bool:
    return any(marker in text for marker in markers)


def is_ehr_system(system: dict[str, Any]) -> bool:
    category = _normalize(system.get("category"))
    if category in EHR_CATEGORIES:
        return True
    if _normalize(system.get("catalog_key")) == "ehr":
        return True
    name = _normalize(system.get("name"))
    if _contains_marker(name, EHR_NAME_MARKERS):
        return True
    return bool(EHR_NAME_TOKENS & _tokens(name))


def kind_for_system(system: dict[str, Any]) -> str:
    if is_ehr_system(system):
        return KIND_EHR
    category = _normalize(system.get("category"))
    if category in CATEGORY_KIND:
        return CATEGORY_KIND[category]
    return kind_from_label(system.get("name") or category or "")


def kind_from_label(label: object) -> str:
    text = _normalize(label)
    if not text:
        return KIND_OTHER
    if _contains_marker(text, EHR_NAME_MARKERS) or bool(EHR_NAME_TOKENS & _tokens(text)):
        return KIND_EHR
    if " ai" in f" {text}" or text.startswith("ai ") or text.endswith(" ai"):
        return KIND_AI
    for kind, markers in KIND_MARKERS:
        if _contains_marker(text, markers):
            return kind
    return KIND_OTHER


def names_match(left: object, right: object) -> bool:
    first = _normalize(left)
    second = _normalize(right)
    if not first or not second:
        return False
    if first == second:
        return True
    shorter, longer = (first, second) if len(first) <= len(second) else (second, first)
    return len(shorter) >= 8 and shorter in longer


def match_system(label: object, systems: Iterable[dict[str, Any]]) -> dict[str, Any] | None:
    hay = _normalize(label)
    if not hay:
        return None
    ranked: list[tuple[int, dict[str, Any]]] = []
    for system in systems:
        name = system.get("name")
        if names_match(hay, name):
            ranked.append((0 if _normalize(name) == hay else 1, system))
            continue
        if names_match(hay, system.get("catalog_key")):
            ranked.append((2, system))
    if not ranked:
        return None
    ranked.sort(key=lambda item: item[0])
    return ranked[0][1]


def classify_endpoint(label: object, systems: Iterable[dict[str, Any]] | None = None) -> EndpointClass:
    text = str(label or "").strip() or "Unnamed endpoint"
    matched = match_system(text, systems or [])
    if matched is not None:
        kind = kind_for_system(matched)
        return EndpointClass(text, kind == KIND_EHR, kind, str(matched.get("name") or text))
    kind = kind_from_label(text)
    return EndpointClass(text, kind == KIND_EHR, kind, None)


def classify_flow(flow: dict[str, Any], systems: Iterable[dict[str, Any]] | None = None) -> FlowClass:
    inventory = list(systems or [])
    source = classify_endpoint(flow.get("source"), inventory)
    destination = classify_endpoint(flow.get("destination"), inventory)
    if source.is_ehr and destination.is_ehr:
        lane = LANE_INSIDE
        kind = KIND_EHR
    elif source.is_ehr or destination.is_ehr:
        lane = LANE_CROSSES
        kind = destination.kind if source.is_ehr else source.kind
    else:
        lane = LANE_OUTSIDE
        kind = _shadowier_kind(source.kind, destination.kind)
    return FlowClass(lane, kind, source, destination)


def _shadowier_kind(left: str, right: str) -> str:
    order = (
        KIND_AI,
        KIND_EMAIL,
        KIND_IMAGING,
        KIND_FILES,
        KIND_MESSAGING,
        KIND_FAX,
        KIND_PHONES,
        KIND_PEOPLE,
        KIND_BILLING,
        KIND_PORTAL,
        KIND_OTHER,
        KIND_EHR,
    )
    ranks = {kind: index for index, kind in enumerate(order)}
    return left if ranks.get(left, 99) <= ranks.get(right, 99) else right


def _risk_rank(value: object) -> int:
    return RISK_ORDER.get(_normalize(value), 9)


def annotate_flow(flow: dict[str, Any], classification: FlowClass) -> dict[str, Any]:
    annotated = dict(flow)
    annotated["ehr_lane"] = classification.lane
    annotated["ehr_lane_label"] = LANE_LABELS[classification.lane]
    annotated["outside_ehr"] = classification.outside_ehr
    annotated["outside_kind"] = classification.kind
    annotated["outside_kind_label"] = KIND_LABELS[classification.kind]
    return annotated


def classify_profile_flows(profile: dict[str, Any]) -> list[tuple[dict[str, Any], FlowClass]]:
    systems = list(profile.get("systems") or [])
    classified: list[tuple[dict[str, Any], FlowClass]] = []
    for flow in profile.get("flows") or []:
        classification = classify_flow(flow, systems)
        classified.append((annotate_flow(flow, classification), classification))
    return classified


def build_ephi_map(profile: dict[str, Any]) -> dict[str, Any]:
    systems = list(profile.get("systems") or [])
    ehr_systems = [system for system in systems if is_ehr_system(system)]
    outside_systems = [system for system in systems if not is_ehr_system(system)]
    classified = classify_profile_flows(profile)
    annotated_flows = [item[0] for item in classified]
    never_touches = [flow for flow in annotated_flows if flow["ehr_lane"] == LANE_OUTSIDE]
    crosses = [flow for flow in annotated_flows if flow["ehr_lane"] == LANE_CROSSES]
    inside = [flow for flow in annotated_flows if flow["ehr_lane"] == LANE_INSIDE]

    def sort_flows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return sorted(rows, key=lambda flow: (_risk_rank(flow.get("risk")), str(flow.get("id") or "")))

    outside_flows = sort_flows(never_touches + crosses)
    high_risk_outside = [
        flow for flow in outside_flows if _normalize(flow.get("risk")) in {"high", "critical"}
    ]
    return {
        "ehr_systems": ehr_systems,
        "outside_systems": outside_systems,
        "flows": annotated_flows,
        "never_touches": sort_flows(never_touches),
        "crosses": sort_flows(crosses),
        "inside": sort_flows(inside),
        "outside_flows": outside_flows,
        "high_risk_outside": high_risk_outside,
        "counts": {
            "systems": len(systems),
            "ehr_systems": len(ehr_systems),
            "outside_systems": len(outside_systems),
            "flows": len(annotated_flows),
            "never_touches": len(never_touches),
            "crosses": len(crosses),
            "inside": len(inside),
            "outside_flows": len(outside_flows),
            "high_risk_outside": len(high_risk_outside),
        },
    }


def annotate_profile(profile: dict[str, Any]) -> dict[str, Any]:
    annotated = deepcopy(profile)
    mapped = build_ephi_map(annotated)
    annotated["flows"] = mapped["flows"]
    return annotated


def strip_derived_ephi_fields(profile: dict[str, Any]) -> dict[str, Any]:
    cleaned = deepcopy(profile)
    for flow in cleaned.get("flows") or []:
        if isinstance(flow, dict):
            for field in DERIVED_FLOW_FIELDS:
                flow.pop(field, None)
    return cleaned
