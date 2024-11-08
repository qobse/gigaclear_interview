import networkx


def cost_calculator(graph_file):
    graph = networkx.read_graphml(graph_file)

    rate_card_a = {
        "cabinet": 1000,
        "trench_verge": 50,
        "trench_road": 100,
        "chamber": 200,
        "pot": 100,
    }

    rate_card_b = {
        "cabinet": 1200,
        "trench_verge": 40,
        "trench_road": 80,
        "chamber": 200,
        "pot": lambda trench_length: 20 * trench_length,
    }

    total_cost_a = 0
    total_coast_b = 0
    cabinet_node = None

    for node in graph.nodes:
        node_data = graph.nodes[node]

        if node_data["type"] == "Cabinet":
            cabinet_node = node
            total_cost_a += rate_card_a["cabinet"]
            total_coast_b += rate_card_b["cabinet"]
        elif node_data["type"] == "Chamber":
            total_cost_a += rate_card_a["chamber"]
            total_coast_b += rate_card_b["chamber"]
        elif node_data["type"] == "Pot":
            total_cost_a += rate_card_a["pot"]

            path = networkx.shortest_path(graph, source=node, target=cabinet_node)
            total_length = sum(
                graph[u][v]["length"] for u, v in zip(path[:-1], path[1:])
            )
            total_coast_b += 20 * total_length

    for edge in graph.edges:
        edge_data = graph.edges[edge]
        edge_type = edge_data["material"]
        edge_length = edge_data["length"]
        if edge_type == "verge":
            total_cost_a += rate_card_a["trench_verge"] * edge_length
            total_coast_b += rate_card_b["trench_verge"] * edge_length
        elif edge_type == "road":
            total_cost_a += rate_card_a["trench_road"] * edge_length
            total_coast_b += rate_card_b["trench_road"] * edge_length

    return total_cost_a, total_coast_b


if __name__ == "__main__":
    total_cost_a, total_coast_b = cost_calculator("problem.graphml")
    print(f"Total cost for rate card A: £{total_cost_a}")
    print(f"Total cost for rate card B: £{total_coast_b}")
