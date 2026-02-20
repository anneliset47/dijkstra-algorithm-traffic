from __future__ import annotations

import heapq
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

Graph = Dict[str, Dict[str, int]]


BASE_GRAPH: Graph = {
    "A": {"B": 16, "C": 16, "D": 10},
    "B": {"A": 16, "C": 5, "E": 16, "I": 17},
    "C": {"A": 16, "B": 5, "F": 9, "H": 10, "I": 16},
    "D": {"A": 10, "E": 12, "H": 18, "I": 7},
    "E": {"B": 16, "D": 12, "I": 12},
    "F": {"C": 9, "G": 8, "I": 22},
    "G": {"F": 8, "H": 7, "I": 16},
    "H": {"C": 10, "D": 18, "G": 7, "I": 14},
    "I": {"B": 17, "C": 16, "D": 7, "E": 12, "F": 22, "G": 16, "H": 14, "J": 3},
    "J": {"I": 3},
}


@dataclass(frozen=True)
class EdgeEvent:
    edge: Tuple[str, str]
    base_weight: int
    traffic_factor: float
    high_impact_event: bool
    impact_factor: float
    final_weight: int


def dijkstra(graph: Graph, source: str) -> Tuple[Dict[str, float], Dict[str, str | None]]:
    distances: Dict[str, float] = {node: float("inf") for node in graph}
    previous: Dict[str, str | None] = {node: None for node in graph}
    distances[source] = 0

    priority_queue: List[Tuple[float, str]] = [(0, source)]
    visited: set[str] = set()

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_node in visited:
            continue
        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            tentative = current_distance + weight
            if tentative < distances[neighbor]:
                distances[neighbor] = tentative
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (tentative, neighbor))

    return distances, previous


def reconstruct_path(previous: Dict[str, str | None], source: str, target: str) -> List[str]:
    path: List[str] = []
    current: str | None = target

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()
    if not path or path[0] != source:
        return []
    return path


def shortest_path(graph: Graph, source: str, target: str) -> Tuple[float, List[str]]:
    distances, previous = dijkstra(graph, source)
    return distances[target], reconstruct_path(previous, source, target)


def apply_rush_hour_traffic(
    graph: Graph,
    *,
    seed: int | None = None,
    mean: float = 2.0,
    std_dev: float = 0.5,
    min_factor: float = 1.0,
    high_impact_prob: float = 0.2,
    impact_min: float = 0.5,
    impact_max: float = 2.0,
) -> Tuple[Graph, List[EdgeEvent]]:
    rng = random.Random(seed)
    modified_graph: Graph = {node: {} for node in graph}
    events: List[EdgeEvent] = []
    seen_edges: set[Tuple[str, str]] = set()

    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            edge = tuple(sorted((node, neighbor)))
            if edge in seen_edges:
                continue
            seen_edges.add(edge)

            traffic_factor = max(min_factor, rng.gauss(mean, std_dev))
            final_weight = weight * traffic_factor

            high_impact_event = rng.random() < high_impact_prob
            impact_factor = 0.0
            if high_impact_event:
                impact_factor = rng.uniform(impact_min, impact_max)
                final_weight += weight * impact_factor

            final_weight_int = max(1, int(round(final_weight)))

            left, right = edge
            modified_graph[left][right] = final_weight_int
            modified_graph[right][left] = final_weight_int

            events.append(
                EdgeEvent(
                    edge=edge,
                    base_weight=weight,
                    traffic_factor=traffic_factor,
                    high_impact_event=high_impact_event,
                    impact_factor=impact_factor,
                    final_weight=final_weight_int,
                )
            )

    return modified_graph, events


def run_demo(source: str = "A", target: str = "J", seed: int = 42) -> dict:
    base_distance, base_path = shortest_path(BASE_GRAPH, source, target)
    rush_graph, events = apply_rush_hour_traffic(BASE_GRAPH, seed=seed)
    rush_distance, rush_path = shortest_path(rush_graph, source, target)

    return {
        "source": source,
        "target": target,
        "seed": seed,
        "base": {"distance": int(base_distance), "path": base_path},
        "rush_hour": {"distance": int(rush_distance), "path": rush_path},
        "edge_events": events,
    }
