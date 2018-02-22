import z3


class Node(object):
    CONSTANT = 0
    VARIABLE = 1

    ADDITION = 10
    SUBTRACTION = 11
    MULTIPLICATION = 12
    DIVISION = 13

    # arithmetic shifts
    LEFT_SHIFT = 20
    RIGHT_SHIFT = 21

    # bitwise logic
    AND = 30
    OR = 31

    VARIABLE_WIDTH = 8  # each variable is one byte

    CONSTANT_CHARS = range(0, 10)
    VARIABLE_CHARS = [chr(x) for x in range(97, 123)]  # lowercase ASCII
    OPERATION_CHARS = {
        '+': ADDITION,
        '-': SUBTRACTION,
        '*': MULTIPLICATION,
        '/': DIVISION,
        '<<': LEFT_SHIFT,
        '>>': RIGHT_SHIFT,
        '&': AND,
        '|': OR
    }

    # TODO: enforce uniqueness of variables!

    def __init__(self, operation, left, right=None):
        self.operation = operation
        self.left = left
        self.right = right

    def __str__(self):
        s = 'Node: %i ' % id(self)
        s += '(Op: %s, ' % str(self.operation)
        if self.operation in [Node.CONSTANT, Node.VARIABLE]:
            s += 'Value: %s)' % str(self.left)
            assert self.right is None  # TODO: this should be elsewhere
        else:  # actual operation
            s += 'Left: %i, ' % id(self.left)
            s += 'Right: %i)' % id(self.right)
        return s

    def print_tree(self):
        print str(self)
        if type(self.left) is Node:
            self.left.print_tree()
        if type(self.right) is Node:
            self.right.print_tree()

    def convert_to_z3(self):
        if self.operation == Node.CONSTANT:
            return self.left  # return for use by caller
        elif self.operation == Node.VARIABLE:
            return z3.BitVec(self.left, Node.VARIABLE_WIDTH)
        else:  # operation
            left = self.left.convert_to_z3()
            right = self.right.convert_to_z3()
            if self.operation == Node.ADDITION:
                return left + right
            elif self.operation == Node.SUBTRACTION:
                return left - right
            elif self.operation == Node.MULTIPLICATION:
                return left * right
            elif self.operation == Node.DIVISION:
                return left / right
            elif self.operation == Node.LEFT_SHIFT:
                return left << right
            elif self.operation == Node.RIGHT_SHIFT:
                return left >> right
            elif self.operation == Node.AND:
                return left & right
            elif self.operation == Node.OR:
                return left | right
            raise LookupError('Unknown operation: %s' % str(self.operation))

    @staticmethod
    def make_constant(value):
        return Node(Node.CONSTANT, value)

    @staticmethod
    def make_variable(variable_name):
        return Node(Node.VARIABLE, variable_name)

    @staticmethod
    def make_operation(operation, left, right):
        return Node(operation, left, right)


def parse_input_line(input_line):
    atoms = input_line.split(' ')
    tree, atoms = parse_atom(atoms)
    assert len(atoms) == 0
    return tree


def parse_atom(atoms):
    assert len(atoms) > 0

    constant = parse_constant(atoms[0])
    if constant is not None:
        return Node.make_constant(constant), atoms[1:]

    variable = parse_variable(atoms[0])
    if variable is not None:
        return Node.make_variable(variable), atoms[1:]

    operation = parse_operation(atoms[0])
    if operation is not None:
        left, atoms = parse_atom(atoms[1:])  # pop operation off of atoms
        right, atoms = parse_atom(atoms)
        return Node.make_operation(operation, left, right), atoms


def parse_constant(atom):
    # only support base 10 for now
    try:
        return int(atom)
    except ValueError:
        return None


def parse_variable(atom):
    for char in atom:
        if char not in Node.VARIABLE_CHARS:
            return None
    return atom


def parse_operation(atom):
    try:
        return Node.OPERATION_CHARS[atom]
    except KeyError:
        return None

if __name__ == '__main__':
    with open('parsetest.txt') as test:
        line = test.readline()
        print 'read line: "%s"' % line
        result = parse_input_line(line)
        result.print_tree()
        expression = result.convert_to_z3()
        z3.solve(0 == expression)
