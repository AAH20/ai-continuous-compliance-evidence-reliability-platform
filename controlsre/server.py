"""Dependency-free HTTP dispatch and local runner."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .adapters import import_framework_catalog
from .coverage import reconcile_population
from .economics import calculate_economics
from .evolution import build_regression_case
from .qualification import qualify_evidence
from .slo import calculate_control_slo


def dispatch(method: str, path: str, payload: dict[str, Any] | None = None) -> tuple[int, dict]:
    if path == "/health" and method == "GET":
        return 200, {"status": "ok", "service": "controlsre", "version": "0.1.0"}
    if method != "POST":
        return (405 if path.startswith("/v1/") else 404), {"error": "method_not_allowed" if path.startswith("/v1/") else "not_found"}
    body = payload or {}
    routes = {
        "/v1/evidence/qualify": lambda: qualify_evidence(body["evidence"], as_of=body["as_of"], max_age_hours=body.get("max_age_hours", 24)),
        "/v1/populations/reconcile": lambda: reconcile_population(body["expected"], body["observed"]),
        "/v1/control-slos": lambda: calculate_control_slo(**body),
        "/v1/economics": lambda: calculate_economics(body),
        "/v1/evolution/regression-cases": lambda: build_regression_case(body),
        "/v1/frameworks/import": lambda: import_framework_catalog(body),
    }
    if path not in routes:
        return 404, {"error": "not_found"}
    try:
        return 200, routes[path]()
    except (KeyError, TypeError, ValueError) as error:
        return 422, {"error": "invalid_request", "detail": str(error)}


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload: dict) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

    def do_GET(self) -> None:
        self._send(*dispatch("GET", self.path))

    def do_POST(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", "0")); payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self._send(400, {"error": "invalid_json"}); return
        self._send(*dispatch("POST", self.path, payload))

    def log_message(self, *_: Any) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8788) -> None:
    ThreadingHTTPServer((host, port), Handler).serve_forever()
