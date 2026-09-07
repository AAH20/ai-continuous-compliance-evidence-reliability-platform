import copy
import json
import tempfile
import unittest
from pathlib import Path

from controlsre.adapters import import_framework_catalog, normalize_inventory
from controlsre.canonical import canonical_json, receipt_sha256
from controlsre.cli import main
from controlsre.coverage import reconcile_population
from controlsre.economics import calculate_economics
from controlsre.evolution import build_regression_case
from controlsre.mapping import detect_mapping_conflicts, propagate_assertion
from controlsre.qualification import qualify_evidence
from controlsre.server import dispatch
from controlsre.slo import calculate_control_slo


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "fixtures" / name).read_text())


class CanonicalTests(unittest.TestCase):
    def test_key_order_does_not_change_receipt(self): self.assertEqual(receipt_sha256({"b": 2, "a": 1}), receipt_sha256({"a": 1, "b": 2}))
    def test_list_order_changes_receipt(self): self.assertNotEqual(receipt_sha256([1, 2]), receipt_sha256([2, 1]))
    def test_canonical_json_is_compact(self): self.assertEqual(canonical_json({"a": 1}), '{"a":1}')
    def test_unicode_is_retained(self): self.assertIn("é", canonical_json({"name": "é"}))


class CoverageTests(unittest.TestCase):
    def test_complete_population(self): self.assertTrue(reconcile_population(["a"], ["a"])["complete"])
    def test_missing_population(self): self.assertEqual(reconcile_population(["a", "b"], ["a"])["missing"], ["b"])
    def test_unexpected_population(self): self.assertEqual(reconcile_population(["a"], ["a", "b"])["unexpected"], ["b"])
    def test_recall(self): self.assertEqual(reconcile_population(["a", "b"], ["a"])["recall"], 0.5)
    def test_duplicates_do_not_inflate_counts(self): self.assertEqual(reconcile_population(["a", "a"], ["a", "a"])["observed_count"], 1)
    def test_empty_expected_rejected(self): self.assertRaises(ValueError, reconcile_population, [], [])
    def test_empty_identifier_rejected(self): self.assertRaises(ValueError, reconcile_population, [""], [""])
    def test_receipt_deterministic(self): self.assertEqual(reconcile_population(["b", "a"], ["a"])["receipt_sha256"], reconcile_population(["a", "b"], ["a"])["receipt_sha256"])
    def test_reference_gap(self): self.assertEqual(reconcile_population(**load("population.json"))["missing"], ["k8s-us-east-2"])
    def test_extra_source_does_not_reduce_recall(self): self.assertEqual(reconcile_population(["a"], ["a", "b"])["recall"], 1)


class QualificationTests(unittest.TestCase):
    def qualify(self, data=None, **kwargs): return qualify_evidence(data or load("evidence-valid.json"), as_of="2026-09-07T12:00:00Z", **kwargs)
    def test_valid_evidence_qualifies(self): self.assertTrue(self.qualify()["qualified"])
    def test_six_gates_present(self): self.assertEqual(len(self.qualify()["gates"]), 6)
    def test_provenance_failure(self):
        data = load("evidence-valid.json"); data["collector"] = ""; self.assertFalse(self.qualify(data)["qualified"])
    def test_integrity_failure(self):
        data = load("evidence-valid.json"); data["payload_sha256"] = "bad"; self.assertFalse(self.qualify(data)["qualified"])
    def test_missing_digest_fails(self):
        data = load("evidence-valid.json"); data.pop("payload_sha256"); self.assertFalse(self.qualify(data)["qualified"])
    def test_scope_failure(self):
        data = load("evidence-valid.json"); data["observed_scope"] = ["production"]; self.assertFalse(self.qualify(data)["qualified"])
    def test_empty_scope_fails(self):
        data = load("evidence-valid.json"); data["expected_scope"] = []; self.assertFalse(self.qualify(data)["qualified"])
    def test_stale_evidence_fails(self): self.assertFalse(qualify_evidence(load("evidence-valid.json"), as_of="2026-09-09T12:00:00Z")["qualified"])
    def test_future_evidence_fails_freshness(self): self.assertFalse(qualify_evidence(load("evidence-valid.json"), as_of="2026-09-07T01:00:00Z")["qualified"])
    def test_relevance_failure(self):
        data = load("evidence-valid.json"); data["target_control_ids"] = ["OTHER"]; self.assertFalse(self.qualify(data)["qualified"])
    def test_empty_targets_fail(self):
        data = load("evidence-valid.json"); data["target_control_ids"] = []; self.assertFalse(self.qualify(data)["qualified"])
    def test_collection_outside_validity_fails(self):
        data = load("evidence-valid.json"); data["valid_from"] = "2026-09-07T09:00:00Z"; self.assertFalse(self.qualify(data)["qualified"])
    def test_collection_outside_audit_fails(self):
        data = load("evidence-valid.json"); data["audit_period_end"] = "2026-09-01T00:00:00Z"; self.assertFalse(self.qualify(data)["qualified"])
    def test_naive_timestamp_rejected(self):
        data = load("evidence-valid.json"); data["collected_at"] = "2026-09-07T08:00:00"; self.assertRaises(ValueError, self.qualify, data)
    def test_nonpositive_freshness_rejected(self): self.assertRaises(ValueError, self.qualify, max_age_hours=0)
    def test_receipt_deterministic(self): self.assertEqual(self.qualify()["receipt_sha256"], self.qualify()["receipt_sha256"])


class SloTests(unittest.TestCase):
    def test_perfect_slo(self): self.assertTrue(calculate_control_slo(required_minutes=100, valid_minutes=100, objective_percent=99)["met"])
    def test_failed_slo(self): self.assertFalse(calculate_control_slo(required_minutes=100, valid_minutes=90, objective_percent=99)["met"])
    def test_burning_state(self): self.assertEqual(calculate_control_slo(required_minutes=100, valid_minutes=90, objective_percent=99)["state"], "burning")
    def test_watch_state(self): self.assertEqual(calculate_control_slo(required_minutes=100, valid_minutes=98.5, objective_percent=99)["state"], "watch")
    def test_healthy_state(self): self.assertEqual(calculate_control_slo(required_minutes=100, valid_minutes=99.5, objective_percent=99)["state"], "healthy")
    def test_zero_required_rejected(self): self.assertRaises(ValueError, calculate_control_slo, required_minutes=0, valid_minutes=0, objective_percent=99)
    def test_excess_valid_rejected(self): self.assertRaises(ValueError, calculate_control_slo, required_minutes=10, valid_minutes=11, objective_percent=99)
    def test_negative_valid_rejected(self): self.assertRaises(ValueError, calculate_control_slo, required_minutes=10, valid_minutes=-1, objective_percent=99)
    def test_invalid_objective_rejected(self): self.assertRaises(ValueError, calculate_control_slo, required_minutes=10, valid_minutes=10, objective_percent=100)
    def test_invalid_elapsed_rejected(self): self.assertRaises(ValueError, calculate_control_slo, required_minutes=10, valid_minutes=10, objective_percent=99, elapsed_fraction=0)
    def test_reference_slo_burns(self): self.assertEqual(calculate_control_slo(**load("control-slo.json"))["state"], "burning")
    def test_receipt_present(self): self.assertEqual(len(calculate_control_slo(required_minutes=10, valid_minutes=10, objective_percent=99)["receipt_sha256"]), 64)


class MappingTests(unittest.TestCase):
    def mapping(self, relationship="equal"): return {"source_control":"A","target_control":"B","relationship":relationship,"strength":1,"rationale":"same objective","source_reference":"urn:test"}
    def test_equal_inherits(self): self.assertTrue(propagate_assertion({"qualified":True}, self.mapping())["inherited_compliance"])
    def test_superset_inherits(self): self.assertTrue(propagate_assertion({"qualified":True}, self.mapping("superset"))["inherited_compliance"])
    def test_subset_does_not_inherit(self): self.assertFalse(propagate_assertion({"qualified":True}, self.mapping("subset"))["inherited_compliance"])
    def test_intersect_does_not_inherit(self): self.assertFalse(propagate_assertion({"qualified":True}, self.mapping("intersect"))["inherited_compliance"])
    def test_conflict_does_not_inherit(self): self.assertFalse(propagate_assertion({"qualified":True}, self.mapping("conflicts_with"))["inherited_compliance"])
    def test_unqualified_does_not_inherit(self): self.assertFalse(propagate_assertion({"qualified":False}, self.mapping())["inherited_compliance"])
    def test_bad_strength_rejected(self):
        mapping = self.mapping(); mapping["strength"] = 2; self.assertRaises(ValueError, propagate_assertion, {"qualified":True}, mapping)
    def test_missing_rationale_rejected(self):
        mapping = self.mapping(); mapping["rationale"] = ""; self.assertRaises(ValueError, propagate_assertion, {"qualified":True}, mapping)
    def test_unknown_relationship_rejected(self): self.assertRaises(ValueError, propagate_assertion, {"qualified":True}, self.mapping("magic"))
    def test_conflict_detection(self): self.assertEqual(len(detect_mapping_conflicts([self.mapping("equal"), self.mapping("subset")])), 1)
    def test_no_false_conflict(self): self.assertEqual(detect_mapping_conflicts([self.mapping("equal"), self.mapping("equal")]), [])


class EconomicsTests(unittest.TestCase):
    def test_reference_cost_per_evidence(self): self.assertEqual(calculate_economics(load("economics.json"))["cost_per_qualified_evidence"], 3.84)
    def test_contract_value_excluded_from_benefit(self):
        data = load("economics.json"); first = calculate_economics(data)["verified_benefit"]; data["confirmed_contract_value"] *= 100; self.assertEqual(calculate_economics(data)["verified_benefit"], first)
    def test_pipeline_excluded_from_benefit(self):
        data = load("economics.json"); first = calculate_economics(data)["verified_benefit"]; data["modeled_pipeline_influenced"] *= 100; self.assertEqual(calculate_economics(data)["verified_benefit"], first)
    def test_approved_margin_enters_benefit(self):
        data = load("economics.json"); first = calculate_economics(data)["verified_benefit"]; data["finance_approved_attributable_margin"] = 10; self.assertEqual(calculate_economics(data)["verified_benefit"], first + 10)
    def test_negative_value_rejected(self):
        data = load("economics.json"); data["model_cost"] = -1; self.assertRaises(ValueError, calculate_economics, data)
    def test_zero_evidence_has_null_unit_cost(self):
        data = load("economics.json"); data["qualified_evidence"] = 0; self.assertIsNone(calculate_economics(data)["cost_per_qualified_evidence"])
    def test_zero_total_cost_has_null_roi(self):
        data = {key: 0 for key in load("economics.json")}; self.assertIsNone(calculate_economics(data)["roi"])
    def test_boolean_rejected(self):
        data = load("economics.json"); data["model_cost"] = True; self.assertRaises(ValueError, calculate_economics, data)
    def test_receipt_deterministic(self): self.assertEqual(calculate_economics(load("economics.json"))["receipt_sha256"], calculate_economics(load("economics.json"))["receipt_sha256"])


class EvolutionTests(unittest.TestCase):
    def incident(self): return {"incident_id":"LOG-02","failure_class":"scope","trigger":"permission loss","expected_safe_behavior":"mark unknown"}
    def test_build_case(self): self.assertTrue(build_regression_case(self.incident())["sanitized"])
    def test_case_id(self): self.assertEqual(build_regression_case(self.incident())["case_id"], "REG-LOG-02")
    def test_missing_field_rejected(self):
        data = self.incident(); data.pop("trigger"); self.assertRaises(ValueError, build_regression_case, data)
    def test_secret_rejected(self):
        data = self.incident(); data["secret"] = "x"; self.assertRaises(ValueError, build_regression_case, data)
    def test_token_rejected(self):
        data = self.incident(); data["token"] = "x"; self.assertRaises(ValueError, build_regression_case, data)
    def test_receipt_deterministic(self): self.assertEqual(build_regression_case(self.incident())["receipt_sha256"], build_regression_case(self.incident())["receipt_sha256"])


class AdapterTests(unittest.TestCase):
    def test_aws_inventory(self): self.assertEqual(normalize_inventory("aws-organizations", [{"Id":"2"},{"Id":"1"}]), ["1","2"])
    def test_kubernetes_inventory(self): self.assertEqual(normalize_inventory("kubernetes", [{"metadata":{"uid":"u1"}}]), ["u1"])
    def test_workflow_inventory(self): self.assertEqual(normalize_inventory("workflow", [{"source_id":"x"}]), ["x"])
    def test_unknown_provider_rejected(self): self.assertRaises(ValueError, normalize_inventory, "unknown", [])
    def test_missing_identifier_rejected(self): self.assertRaises(ValueError, normalize_inventory, "workflow", [{}])
    def test_duplicate_identifier_rejected(self): self.assertRaises(ValueError, normalize_inventory, "workflow", [{"source_id":"x"},{"source_id":"x"}])
    def test_framework_import(self): self.assertEqual(import_framework_catalog(load("frameworks.json"))["framework_count"], 4)
    def test_duplicate_framework_rejected(self): self.assertRaises(ValueError, import_framework_catalog, {"frameworks":[{"urn":"a"},{"urn":"a"}]})
    def test_framework_list_required(self): self.assertRaises(ValueError, import_framework_catalog, {"frameworks":"bad"})


class ApiTests(unittest.TestCase):
    def test_health(self): self.assertEqual(dispatch("GET", "/health")[0], 200)
    def test_not_found(self): self.assertEqual(dispatch("GET", "/missing")[0], 404)
    def test_method_not_allowed(self): self.assertEqual(dispatch("GET", "/v1/economics")[0], 405)
    def test_qualification_endpoint(self): self.assertEqual(dispatch("POST", "/v1/evidence/qualify", {"evidence":load("evidence-valid.json"),"as_of":"2026-09-07T12:00:00Z"})[0], 200)
    def test_coverage_endpoint(self): self.assertEqual(dispatch("POST", "/v1/populations/reconcile", load("population.json"))[1]["missing"], ["k8s-us-east-2"])
    def test_slo_endpoint(self): self.assertEqual(dispatch("POST", "/v1/control-slos", load("control-slo.json"))[0], 200)
    def test_economics_endpoint(self): self.assertEqual(dispatch("POST", "/v1/economics", load("economics.json"))[0], 200)
    def test_framework_endpoint(self): self.assertEqual(dispatch("POST", "/v1/frameworks/import", load("frameworks.json"))[0], 200)
    def test_invalid_payload(self): self.assertEqual(dispatch("POST", "/v1/control-slos", {})[0], 422)


class CliTests(unittest.TestCase):
    def run_output(self, command, fixture, extra=None):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "result.json"; args = [command, str(ROOT / "fixtures" / fixture), *(extra or []), "--output", str(output)]
            self.assertEqual(main(args), 0); return json.loads(output.read_text())
    def test_coverage_cli(self): self.assertEqual(self.run_output("coverage", "population.json")["recall"], 0.8)
    def test_slo_cli(self): self.assertEqual(self.run_output("slo", "control-slo.json")["state"], "burning")
    def test_economics_cli(self): self.assertEqual(self.run_output("economics", "economics.json")["cost_per_qualified_evidence"], 3.84)
    def test_qualify_cli(self): self.assertTrue(self.run_output("qualify", "evidence-valid.json", ["--as-of","2026-09-07T12:00:00Z"])["qualified"])


if __name__ == "__main__":
    unittest.main()
