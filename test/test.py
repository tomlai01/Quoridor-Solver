from src.SmartPlayer import SmartPlayer
from src.State import State

state = State(2)
node = SmartPlayer.Node(0, state)
neighbors = node.get_neighbors()
print(neighbors)

