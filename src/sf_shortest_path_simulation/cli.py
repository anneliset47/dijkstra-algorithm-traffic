from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .sf_shortest_path_simulation import run_demo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run shortest-path simulation for San Francisco landmarks."
    )
    parser.add_argument("--source", default="A", help="Start node (default: A)")
    parser.add_argument("--target", default="J", help="Target node (default: J)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for rush-hour scenario")
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )
    parser.add_argument(
        "--show-edge-events",
        action="store_true",
        help="Include per-edge rush-hour simulation details in text output",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = run_demo(source=args.source, target=args.target, seed=args.seed)

    if args.output == "json":
        payload = {
            **result,
            "edge_events": [asdict(event) for event in result["edge_events"]],
        }
        print(json.dumps(payload, indent=2))
        return

    print("San Francisco Shortest Path Simulation")
    print(f"Source: {result['source']}  Target: {result['target']}  Seed: {result['seed']}")
    print("\nScenario 1 (Base):")
    print(f"  Path: {' -> '.join(result['base']['path'])}")
    print(f"  Travel time: {result['base']['distance']} minutes")

    print("\nScenario 2 (Rush Hour):")
    print(f"  Path: {' -> '.join(result['rush_hour']['path'])}")
    print(f"  Travel time: {result['rush_hour']['distance']} minutes")

    if args.show_edge_events:
        print("\nRush-hour edge events:")
        for event in result["edge_events"]:
            print(
                "  "
                f"{event.edge[0]}-{event.edge[1]} | base={event.base_weight} | "
                f"traffic={event.traffic_factor:.2f} | "
                f"high_impact={event.high_impact_event} | "
                f"impact={event.impact_factor:.2f} | final={event.final_weight}"
            )


if __name__ == "__main__":
    main()
