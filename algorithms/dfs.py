from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [initial]   # pilha (LIFO)
        explored: set = set()
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            node = frontier.pop()

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=node.cost,
                )

            if node.tiles in explored:
                continue

            if node.cost >= self.depth_limit:
                continue

            explored.add(node.tiles)
            nodes_expanded += 1

            for child in node.neighbors():
                nodes_generated += 1
                if child.tiles not in explored:
                    frontier.append(child)

        return SearchResult(solution=None, nodes_expanded=nodes_expanded, nodes_generated=nodes_generated, max_frontier_size=max_frontier_size)
