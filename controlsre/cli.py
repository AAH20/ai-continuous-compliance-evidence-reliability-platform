"""ControlSRE command-line interface."""

import argparse
import json
from pathlib import Path
from typing import Any

from .coverage import reconcile_population
from .economics import calculate_economics
from .qualification import qualify_evidence
from .server import serve
from .slo import calculate_control_slo


def load(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def emit(payload: dict, output: str | None) -> None:
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if output: Path(output).write_text(text, encoding="utf-8")
    else: print(text, end="")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="controlsre", description="Control reliability engineering for continuous compliance evidence")
    sub = root.add_subparsers(dest="command", required=True)
    qualify = sub.add_parser("qualify"); qualify.add_argument("input"); qualify.add_argument("--as-of", required=True); qualify.add_argument("--max-age-hours", type=int, default=24); qualify.add_argument("--output")
    coverage = sub.add_parser("coverage"); coverage.add_argument("input"); coverage.add_argument("--output")
    slo = sub.add_parser("slo"); slo.add_argument("input"); slo.add_argument("--output")
    economics = sub.add_parser("economics"); economics.add_argument("input"); economics.add_argument("--output")
    server = sub.add_parser("serve"); server.add_argument("--host", default="127.0.0.1"); server.add_argument("--port", type=int, default=8788)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "serve": serve(args.host, args.port); return 0
    data = load(args.input)
    if args.command == "qualify": result = qualify_evidence(data, as_of=args.as_of, max_age_hours=args.max_age_hours)
    elif args.command == "coverage": result = reconcile_population(data["expected"], data["observed"])
    elif args.command == "slo": result = calculate_control_slo(**data)
    else: result = calculate_economics(data)
    emit(result, args.output); return 0


if __name__ == "__main__":
    raise SystemExit(main())
