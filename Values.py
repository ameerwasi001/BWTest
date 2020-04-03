class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        return None, self.IllegalOperationError(other)

    def subbed_by(self, other):
        return None, self.IllegalOperationError(other)

    def multed_by(self, other):
        return None, self.IllegalOperationError(other)

    def dived_by(self, other):
        return None, self.IllegalOperationError(other)

    def copy(self):
        raise Exception("No copy method defined")

    def IllegalOperationError(self, other=None):
        if not other: other = self
        return RTError(
            self.pos_start, self.pos_end,
            self.context,
            'Illegal Operation'
        )

class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = float(value)

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, self.IllegalOperationError(other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, self.IllegalOperationError(other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, self.IllegalOperationError(other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value != 0:
                return Number(self.value / other.value).set_context(self.context), None
            else:
                return None, RTError(
                    self.pos_start, other.pos_end,
                    self.context,
                    "Division by Zero"
                )
        else:
            return None, self.IllegalOperationError(other)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def lt(self, other):
        if isinstance(other, Number):
            return Boolean(self.value < other.value).set_context(self.context), None
        else:
            return None, self.IllegalOperationError(other)

    def lte(self, other):
        if isinstance(other, Number):
            return Boolean(self.value <= other.value).set_context(self.context), None
        else:
            return None, self.IllegalOperationError(other)

    def gt(self, other):
        if isinstance(other, Number):
            return Boolean(self.value > other.value).set_context(self.context), None
        else:
            return None, self.IllegalOperationError(other)

    def gte(self, other):
        if isinstance(other, Number):
            return Boolean(self.value >= other.value).set_context(self.context), None
        else:
            return None, self.IllegalOperationError(other)

    def ee(self, other):
        if isinstance(other, Number):
            return Boolean(self.value == other.value).set_context(self.context), None
        else:
            return None, self.IllegalOperationError(other)

    def ne(self, other):
        if isinstance(other, Number):
            return Boolean(self.value != other.value).set_context(self.context), None
        else:
            return None, self.IllegalOperationError(other)

    def is_true(self):
        return self.value != 0

    def notted(self):
        return Boolean(not self.is_true()).set_context(self.context), None

    def anded(self, other):
        return Boolean((self.is_true()) and (other.is_true())).set_context(self.context), None

    def ored(self, other):
        return Boolean((self.is_true()) or (other.is_true())).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f"{self.value}"


class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, self.IllegalOperationError(other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * int(other.value)).set_context(self.context), None
        else:
            return None, self.IllegalOperationError(other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if len(self.value) > other.value:
                return String(self.value[int(other.value)]).set_context(self.context), None
            else:
                return None, RTError(
                    self.pos_start, other.pos_end,
                    self.context,
                    "List out of range"
                )
        else:
            return None, self.IllegalOperationError(other)

    def __int__(self):
        return str(self.value)

    def __float__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

    def is_true(self):
        return len(self.value) != 0

    def ee(self, other):
        if isinstance(other, String):
            return Boolean(self.value == other.value).set_context(self.context), None
        else:
            return Boolean(0), None

    def ne(self, other):
        if isinstance(other, String):
            return Boolean(self.value != other.value).set_context(self.context), None
        else:
            return Boolean(1), None

    def notted(self):
        return Boolean(not self.is_true()).set_context(self.context), None

    def anded(self, other):
        return Boolean((self.is_true()) and (other.is_true())).set_context(self.context), None

    def ored(self, other):
        return Boolean((self.is_true()) or (other.is_true())).set_context(self.context), None

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f"{self.value}"

class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def is_true(self):
        return len(self.elements) > 0

    def notted(self):
        return Boolean(not self.is_true()).set_context(self.context), None

    def anded(self, other):
        return Boolean((self.is_true()) and (other.is_true())).set_context(self.context), None

    def ored(self, other):
        return Boolean((self.is_true()) or (other.is_true())).set_context(self.context), None

    def copy(self):
        copy = List(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'


class Boolean(Number):
    def __init__(self, state):
        super().__init__(state)
        self.state = state

    def copy(self):
        copy = Boolean(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return 'true' if self.state else 'false'

class nilObject(Number):
    def __init__(self):
        super().__init__(0)

    def copy(self):
        copy = nilObject()
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return 'nil'

nil = nilObject()
false = Boolean(0)
true = Boolean(1)
