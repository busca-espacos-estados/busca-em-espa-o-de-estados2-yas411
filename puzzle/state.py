from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Movimentos possíveis: (nome_da_ação, deslocamento_no_índice)
# O blank se move para cima (-3), baixo (+3), esquerda (-1), direita (+1)
MOVES = [
    ("cima",    -3),
    ("baixo",   +3),
    ("esquerda", -1),
    ("direita",  +1),
]

# Colunas de cada índice (0-8) para impedir "wrap" horizontal
COL = [0, 1, 2, 0, 1, 2, 0, 1, 2]


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado."""
        children = []
        bi = self.blank_index
        for action, delta in MOVES:
            ni = bi + delta
            # Verifica se o novo índice está dentro do tabuleiro
            if ni < 0 or ni >= 9:
                continue
            # Impede wrap horizontal (esquerda/direita entre colunas 0 e 2)
            if action == "esquerda" and COL[bi] == 0:
                continue
            if action == "direita" and COL[bi] == 2:
                continue

            new_tiles = list(self.tiles)
            new_tiles[bi], new_tiles[ni] = new_tiles[ni], new_tiles[bi]
            children.append(State(
                tiles=tuple(new_tiles),
                parent=self,
                action=action,
                cost=self.cost + 1,
            ))
        return children

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este."""
        node, sequence = self, []
        while node is not None:
            sequence.append(node)
            node = node.parent
        sequence.reverse()
        return sequence

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este."""
        return [state.action for state in self.path() if state.action is not None]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
