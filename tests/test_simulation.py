import unittest

from sf_shortest_path_simulation.sf_shortest_path_simulation import BASE_GRAPH, apply_rush_hour_traffic, shortest_path


class SimulationTests(unittest.TestCase):
    def test_base_shortest_path(self) -> None:
        distance, path = shortest_path(BASE_GRAPH, "A", "J")
        self.assertEqual(distance, 20)
        self.assertEqual(path, ["A", "D", "I", "J"])

    def test_rush_hour_reproducible_with_seed(self) -> None:
        graph_a, _ = apply_rush_hour_traffic(BASE_GRAPH, seed=123)
        graph_b, _ = apply_rush_hour_traffic(BASE_GRAPH, seed=123)
        self.assertEqual(graph_a, graph_b)


if __name__ == "__main__":
    unittest.main()
