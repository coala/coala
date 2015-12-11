from math import sqrt

from coalib.misc.Decorators import generate_repr


@generate_repr()
class CountVector:
    def __init__(self, name, conditions=None, weightings=None):
        """
        Creates a new count vector.

        :param name:       The name of the variable in the original code.
        :param conditions: The counting conditions as list of function objects,
                           each shall return true when getting data indicating
                           that this occurrence should be counted.
        :param weightings: Optional factors to weight counting conditions.
                           Defaults to 1 for all conditions.
        """
        self.name = name
        self.conditions = conditions if conditions is not None else []
        self.count_vector = [0 for elem in self.conditions]
        self.unweighted = [0 for elem in self.conditions]
        self.weightings = weightings
        if self.weightings is None:
            self.weightings = [1 for elem in self.conditions]

        assert len(self.count_vector) is len(self.weightings)

    def create_null_vector(self, name):
        """
        Creates a new CountVector object with the same counting conditions
        and weightings but initializes it to zero.

        :return: A CountVector object.
        """
        return CountVector(name, self.conditions, self.weightings)

    def count_reference(self, *args, **kwargs):
        """
        Counts the reference to the variable under the conditions held in this
        object.

        Any arguments or kwarguments will be passed to all conditions.
        """
        for i in range(len(self.conditions)):
            if self.conditions[i](*args, **kwargs):
                self.count_vector[i] += self.weightings[i]
                self.unweighted[i] += 1

    def __str__(self):
        return str(self.count_vector)

    def __len__(self):
        return len(self.count_vector)

    def __iter__(self):
        return iter(self.count_vector)

    def __abs__(self):
        return sqrt(sum(x**2 for x in self))

    def maxabs(self, other):
        """
        Calculates the absolute value of a vector that has the maximum
        entries row-wise of both given vectors. This can be used as
        normalization since this value is guaranteed to be bigger or equal
        the difference value of those two vectors.

        :param other: The vector to normalize with.
        :return:      A float value bigger or equal than the difference
                      between self and other.
        """
        return sqrt(sum(max(x, y)**2 for x, y in zip(self, other)))

    def difference(self, other):
        """
        Calculates an absolute difference value. 0 means no difference,
        i.e. the count vectors are identical.

        :param other: The CountVector to calculate the difference to.
        :return:      An absolute difference value.
        """
        assert isinstance(other, CountVector)
        assert len(other) == len(self)

        return sqrt(sum((x-y)**2 for x, y in zip(self, other)))
