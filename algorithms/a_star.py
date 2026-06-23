import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

GOAL_POS = {val: idx for idx, val in enumerate((1, 2, 3, 4, 5, 6, 7, 8, 0))}


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan — heurística admissível e consistente."""
        distance = 0
        for idx, val in enumerate(state.tiles):
            if val == 0:
                continue
            goal_idx = GOAL_POS[val]
            distance += abs(idx // 3 - goal_idx // 3) + abs(idx % 3 - goal_idx % 3)
        return distance

    def search(self, initial: State) -> SearchResult:
        # f = g + h  (g = custo acumulado, h = heurística)
        h0 = self.heuristic(initial)
        # heap entries: (f, tie-breaker, state)
        counter = 0
        heap = [(h0, counter, initial)]
        explored: dict = {}          # tiles -> menor g visto
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while heap:
            max_frontier_size = max(max_frontier_size, len(heap))
            f, _, node = heapq.heappop(heap)

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=node.cost,
                )

            if node.tiles in explored and explored[node.tiles] <= node.cost:
                continue

            explored[node.tiles] = node.cost
            nodes_expanded += 1

            for child in node.neighbors():
                nodes_generated += 1
                if child.tiles not in explored or explored[child.tiles] > child.cost:
                    f_child = child.cost + self.heuristic(child)
                    counter += 1
                    heapq.heappush(heap, (f_child, counter, child))

        return SearchResult(solution=None, nodes_expanded=nodes_expanded, nodes_generated=nodes_generated, max_frontier_size=max_frontier_size)
