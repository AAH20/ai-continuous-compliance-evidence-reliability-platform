"""Generate deterministic reference artifacts consumed by the public dashboard."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from controlsre.adapters import import_framework_catalog
from controlsre.coverage import reconcile_population
from controlsre.economics import calculate_economics
from controlsre.qualification import qualify_evidence
from controlsre.slo import calculate_control_slo


FIXTURES = ROOT / "fixtures"
OUTPUT = ROOT / "public" / "api" / "v1"


def load(name):
    return json.loads((FIXTURES / name).read_text())


def write(name, payload):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


write("evidence-qualified.json", qualify_evidence(load("evidence-valid.json"), as_of="2026-09-07T12:00:00Z"))
write("population.json", reconcile_population(**load("population.json")))
write("control-slo.json", calculate_control_slo(**load("control-slo.json")))
write("economics.json", calculate_economics(load("economics.json")))
write("frameworks.json", import_framework_catalog(load("frameworks.json")))
write("failure-scenarios.json", load("failure-scenarios.json"))
write("index.json", {"release": "0.1.0", "evidence_level": "SYNTHETIC_REFERENCE", "artifacts": ["evidence-qualified.json", "population.json", "control-slo.json", "economics.json", "frameworks.json", "failure-scenarios.json"]})
