import dataclasses
import math


class CutTree:
    @dataclasses.dataclass
    class Node:
        n_leaves_cut: int
        is_terminal_node: bool = False
        children: dict[int, 'CutTree.Node'] = dataclasses.field(default_factory=dict)

    def __init__(self, num_nodes):
        self.n = num_nodes
        self.head = CutTree.Node(0)

    def cut(self, path: list[int]):

        # Find the terminal node
        # It will be the last node in the path
        #  or the first terminal node we find along the way
        node = self.head
        for i in path:
            if node.is_terminal_node:
                # This means we didn't reach the end of the path
                #  -> so the path cuts nodes that have already been cut
                # So we can just return
                return

            if i not in node.children:
                # This path has not been followed before,
                # so we will build it as we go
                node.children[i] = CutTree.Node(0)

            node = node.children[i]

        # We've reached the end of the line
        # The node we have is the terminal (cut) node
        node.is_terminal_node = True

        # How many leaves did we already know where cut?
        already_cut = node.n_leaves_cut

        # How many leaves just got cut?
        node.n_leaves_cut = math.factorial(self.n - len(path))
        new_leaves_cut = node.n_leaves_cut - already_cut

        # Now we need to update all the parents with the difference
        node = self.head
        for i in path:
            if node.is_terminal_node:
                break
            node.n_leaves_cut += new_leaves_cut

            node = node.children[i]
            # If we ended up descending the full path in the first descent
            # then the last child will be a new terminal node
            # which already has an accurate n_leaves_cut
            # -> so we don't need to modify the last node in this descent

    def n_leaves_cut(self):
        return self.head.n_leaves_cut

    def fraction_leaves_covered(self):
        # Subtract 1 from n because the first node is fixed
        return self.n_leaves_cut() / math.factorial(self.n - 1)
