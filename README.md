# San Francisco Shortest Path Simulation

[![CI](https://github.com/anneliset47/sf-shortest-path-simulation/actions/workflows/ci.yml/badge.svg)](https://github.com/anneliset47/sf-shortest-path-simulation/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Recruiter-ready Python project that models route optimization between San Francisco landmarks using Dijkstra’s algorithm under two conditions:
- **Scenario 1 (Base Case):** average travel times
- **Scenario 2 (Rush Hour):** stochastic congestion + low-probability high-impact events

The original notebook implementation has been converted into a reusable Python package and CLI for cleaner engineering practices and reproducible runs.

## Why this project matters

This project demonstrates practical software engineering and algorithmic skills:
- graph modeling with weighted adjacency maps
- shortest-path optimization with a heap-based Dijkstra implementation
- uncertainty modeling with probabilistic simulation
- reproducible experimentation via deterministic random seeds
- packaging, testing, and CLI ergonomics for maintainability

## Results snapshot

- **Base shortest path (A → J):** `A -> D -> I -> J`
- **Base travel time:** `20` minutes
- **Rush-hour travel time:** varies by seed/simulation

## Repository structure

```text
.
├── notebooks/
│   ├── sf_shortest_path_simulation.ipynb
│   └── sf_shortest_path_simulation.py   # converted script
├── report/
│   └── sf_shortest_path_simulation_report.pdf
├── src/
│   └── sf_shortest_path_simulation/
│       ├── __init__.py
│       ├── simulation.py                # core graph + simulation logic
│       └── cli.py                       # command-line interface
├── tests/
│   └── test_simulation.py
├── pyproject.toml
└── README.md
```

## Quickstart

### 1) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install the project

```bash
pip install -e .
```

### 3) Run the simulation

```bash
sf-shortest-path --source A --target J --seed 42
```

### Optional: JSON output + edge-level event details

```bash
sf-shortest-path --source A --target J --seed 42 --output json
sf-shortest-path --source A --target J --seed 42 --show-edge-events
```

## Reproducibility

- Rush-hour randomness is controlled through `--seed`.
- Running with the same seed yields identical rush-hour edge weights.
- Unit tests verify both deterministic base-path behavior and seeded reproducibility.

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Engineering notes

- Core algorithm and simulation logic live in `src/sf_shortest_path_simulation/simulation.py`.
- CLI parsing and output formatting live in `src/sf_shortest_path_simulation/cli.py`.
- The notebook conversion entrypoint is `notebooks/sf_shortest_path_simulation.py`.

## Authoring

- Annelise Thorn
- Juliana Zweng






