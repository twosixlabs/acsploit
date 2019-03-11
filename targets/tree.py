import argparse


# A Red-Black Tree that only supports insertions
#  as that's all we need to demonstrate ACsploit
class RedBlackNode:
    BLACK = 'black'
    RED = 'red'
    rotations = 0

    @staticmethod
    def make_tree():
        root = RedBlackNode()
        return root

    @classmethod
    def get_rotations(cls):
        return cls.rotations

    def __init__(self, value=None, color=BLACK, parent=None):
        self.value = value
        self.color = color
        self.parent = parent
        self.left = None
        self.right = None

    def pprint(self, depth=0):
        prefix = '\t' * depth
        print('%sValue: %r' % (prefix, self.value))
        print('%sColor: %r' % (prefix, self.color))
        print('%sLeft:' % prefix)
        if self.left is not None:
            self.left.pprint(depth=depth+1)
        print('%sRight:' % prefix)
        if self.right is not None:
            self.right.pprint(depth=depth + 1)

    def _root(self):
        target = self
        while target.parent is not None:
            target = target.parent
        return target

    def _uncle(self):
        if self.parent is None:
            return None
        if self.parent.parent is None:
            return None
        if self.parent is self.parent.parent.left:
            return self.parent.parent.right
        else:
            return self.parent.parent.left

    def _rotate_left(self):
        RedBlackNode.rotations += 1
        print('Rotating left')

        parent = self.parent
        new_center = self.right

        self.right = new_center.left
        new_center.left = self
        self.parent = new_center
        new_center.parent = parent

        if self.right is not None:
            self.right.parent = self

        if parent is not None:
            if parent.left is self:
                parent.left = new_center
            else:
                parent.right = new_center

    def _rotate_right(self):
        RedBlackNode.rotations += 1
        print('Rotating right')

        parent = self.parent
        new_center = self.left

        self.left = new_center.right
        new_center.right = self
        self.parent = new_center
        new_center.parent = parent

        if self.left is not None:
            self.left.parent = self

        if parent is not None:
            if parent.left is self:
                parent.left = new_center
            else:
                parent.right = new_center

    def _repair(self):
        if self.parent is None:  # insertion at root
            self.color = RedBlackNode.BLACK  # recolor root to black
        elif self.parent.color == RedBlackNode.BLACK:  # parent is black
            return  # everything is fine
        elif self.parent.color == RedBlackNode.RED and self._uncle().color == RedBlackNode.RED:  # parent and uncle are red
            # recolor parent and uncle black and grandparent red
            self.parent.color = RedBlackNode.BLACK
            self._uncle().color = RedBlackNode.BLACK
            self.parent.parent.color = RedBlackNode.RED
            # maintain invariants on grandparent
            RedBlackNode._repair(self.parent.parent)
        else:  # parent is red and uncle is black
            # rotate the current node into its grandparent's position
            target = self
            # rotate the current node into the 'outside' of the tree if it's on the inside
            if self is self.parent.right and self.parent is self.parent.parent.left:
                RedBlackNode._rotate_left(self.parent)
                target = self.left
            elif self is self.parent.left and self.parent is self.parent.parent.right:
                RedBlackNode._rotate_right(self.parent)
                target = self.right
            # recolor the parent and grandparent
            target.parent.color = RedBlackNode.BLACK
            if target.parent.parent is not None:
                target.parent.parent.color = RedBlackNode.RED
            # now rotate the grandparent
            if target is target.parent.left:
                RedBlackNode._rotate_right(target.parent.parent)
            else:
                RedBlackNode._rotate_left(target.parent.parent)

    def _insert_recursive(self, new_value):
        if self.value is None:
            self.value = new_value
            self.color = RedBlackNode.RED
            self.left = RedBlackNode(parent=self)
            self.right = RedBlackNode(parent=self)
            return self
        elif new_value < self.value:
            return self.left._insert_recursive(new_value)
        else:
            return self.right._insert_recursive(new_value)

    def insert(self, new_value):
        print('Inserting %r' % new_value)
        new_node = self._insert_recursive(new_value)
        new_node._repair()

        # find and return the new root
        return self._root()


def main():
    parser = argparse.ArgumentParser(description='Partial implementation of a Red-Black Tree to demonstrate ACsploit')
    parser.add_argument('value', metavar='VALUE', nargs='+', type=int, help='Values to add to the tree')

    args = parser.parse_args()

    tree = RedBlackNode.make_tree()
    for value in args.value:
        tree = tree.insert(value)

    print('The final tree structure looks like:')
    tree.pprint()
    print('%i rotations occurred while inserting %i elements' % (tree.get_rotations(), len(args.value)))


if __name__ == '__main__':
    main()
