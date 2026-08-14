from __future__ import annotations

import unittest
from pathlib import Path

from small_practice_security_kit.ephi_map import (
    LANE_CROSSES,
    LANE_INSIDE,
    LANE_OUTSIDE,
    annotate_profile,
    build_ephi_map,
    classify_endpoint,
    classify_flow,
    is_ehr_system,
    strip_derived_ephi_fields,
)
from small_practice_security_kit.packet import ephi_flow_map
from small_practice_security_kit.profile import load_profile


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "samples" / "family_dental_clinic.yaml"


class EphiMapTests(unittest.TestCase):
    def test_ehr_system_detection(self) -> None:
        self.assertTrue(is_ehr_system({"name": "Cloud EHR", "category": "EHR"}))
        self.assertTrue(is_ehr_system({"name": "Practice chart", "category": "EMR"}))
        self.assertFalse(is_ehr_system({"name": "Dental Imaging Workstation", "category": "Imaging"}))
        self.assertFalse(is_ehr_system({"name": "General AI Assistant", "category": "AI drafting"}))

    def test_unmatched_endpoints_use_plain_language(self) -> None:
        self.assertTrue(classify_endpoint("Staff email").kind == "email")
        self.assertEqual(classify_endpoint("Front desk notes").kind, "people_process")
        self.assertEqual(classify_endpoint("Provider conversation").kind, "people_process")
        self.assertTrue(classify_endpoint("Cloud EHR").is_ehr)

    def test_family_dental_sample_splits_outside_ehr_paths(self) -> None:
        profile = load_profile(SAMPLE)
        mapped = build_ephi_map(profile)
        by_id = {flow["id"]: flow for flow in mapped["flows"]}

        self.assertEqual(by_id["FLOW-001"]["ehr_lane"], LANE_CROSSES)
        self.assertEqual(by_id["FLOW-002"]["ehr_lane"], LANE_CROSSES)
        self.assertEqual(by_id["FLOW-003"]["ehr_lane"], LANE_OUTSIDE)
        self.assertEqual(by_id["FLOW-004"]["ehr_lane"], LANE_OUTSIDE)
        self.assertEqual(by_id["FLOW-005"]["ehr_lane"], LANE_OUTSIDE)
        self.assertEqual(by_id["FLOW-006"]["ehr_lane"], LANE_OUTSIDE)

        self.assertEqual(by_id["FLOW-003"]["outside_kind"], "email")
        self.assertEqual(by_id["FLOW-004"]["outside_kind"], "imaging")
        self.assertEqual(by_id["FLOW-005"]["outside_kind"], "ai")
        self.assertEqual(by_id["FLOW-006"]["outside_kind"], "ai")

        self.assertGreaterEqual(mapped["counts"]["never_touches"], 4)
        self.assertGreaterEqual(mapped["counts"]["crosses"], 2)
        self.assertEqual(mapped["counts"]["inside"], 0)
        self.assertGreaterEqual(mapped["counts"]["outside_systems"], 6)

    def test_inside_ehr_flow_stays_in_chart(self) -> None:
        systems = [{"name": "Cloud EHR", "category": "EHR"}]
        classification = classify_flow(
            {"source": "Cloud EHR", "destination": "Cloud EHR"},
            systems,
        )
        self.assertEqual(classification.lane, LANE_INSIDE)
        self.assertFalse(classification.outside_ehr)

    def test_packet_leads_with_outside_ehr_section(self) -> None:
        profile = load_profile(SAMPLE)
        text = ephi_flow_map(profile)
        self.assertIn("Patient Data Outside the EHR", text)
        self.assertIn("Never touches the EHR", text)
        self.assertIn("Leaves or enters the EHR", text)
        self.assertIn("Staff email", text.split("## Patient Data Outside the EHR", 1)[1])
        self.assertNotIn("## Systems Outside the EHR", text)
        self.assertNotIn("## All Systems", text)
        self.assertNotIn("## Traceability Summary", text)

    def test_annotate_and_strip_keep_profile_clean(self) -> None:
        profile = load_profile(SAMPLE)
        annotated = annotate_profile(profile)
        self.assertIn("ehr_lane", annotated["flows"][0])
        self.assertNotIn("ehr_lane", profile["flows"][0])
        cleaned = strip_derived_ephi_fields(annotated)
        self.assertNotIn("ehr_lane", cleaned["flows"][0])
        self.assertIn("ehr_lane", annotated["flows"][0])


if __name__ == "__main__":
    unittest.main()
