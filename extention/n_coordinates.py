import math
from typing import List, Optional


class NVector:
    """
    Represents a vector in the hexagonal grid. It can calculate various vector operations.
    """

    def __init__(self, d_x: int = 0, d_y: int = 0):
        """
        Constructor for the Vector class.

        :param d_x: The x-coordinate of the vector.
        :param d_y: The y-coordinate of the vector.
        """
        self.d_x = d_x
        self.d_y = d_y

    def magnitude(self) -> float:
        """
        Calculates the length of the vector.

        :return: The length of the vector.
        """
        return (self.d_x ** 2 + self.d_y ** 2) ** 0.5

    def dot_product(self, other: 'NVector'):
        """
        Calculates the dot product of two vectors.

        :param other: The other vector to calculate the dot product with.
        :return: The dot product of the two vectors.
        """
        return self.d_x * other.d_x + self.d_y * other.d_y

    def cross_product(self, other: 'NVector'):
        """
        Calculates the cross product of two vectors.

        :param other: The other vector to calculate the cross product with.
        :return: The cross product of the two vectors.
        """
        return self.d_x * other.d_y - self.d_y * other.d_x

    def scalar_product(self, scalar: int):
        """
        Extends the vector by a scalar.

        :param scalar: The scalar to extend the vector by.
        :return: The extended vector.
        """
        return NVector(self.d_x * scalar, self.d_y * scalar)

    def addition(self, other: 'NVector'):
        """
        Adds two vectors.

        :param other: The other vector to add.
        :return: The sum of the two vectors as a new vector object.
        """
        return NVector(self.d_x + other.d_x, self.d_y + other.d_y)

    def subtraction(self, other: 'NVector'):
        """
        Subtracts two vectors.

        :param other: The other vector to subtract.
        :return: The difference of the two vectors as a new vector object.
        """
        return NVector(self.d_x - other.d_x, self.d_y - other.d_y)

    def get_arc_tangent(self) -> float:
        """
        Calculates the arc tangent of the vector.

        :return: A radiant in float.
        """
        return math.atan2(self.d_y, self.d_x)

    def are_identically(self, other: 'NVector'):
        """
        Compares two vectors.

        :param other: The other vector to compare to.
        :return: True if the vectors are equal, false otherwise.
        """
        return self.d_x == other.d_x and self.d_y == other.d_y

    def are_equal(self, other: 'NVector'):
        """
        Checks if two vectors have the same magnitude and direction.

        :param other: The other vector to compare to.
        :return: True if the vectors are equal, false otherwise.
        """
        return self.magnitude() == other.magnitude() and self.get_arc_tangent() == other.get_arc_tangent()

    @property
    def directions(self) -> List['NVector']:
        """
        Gets the six neighbors of the vector.

        :return: A list of the six neighbors of the vector.
        """
        return [
            NVector(1, -1),  # UP RIGHT
            NVector(2, 0),  # RIGHT
            NVector(1, 1),  # DOWN RIGHT
            NVector(-1, 1),  # DOWN LEFT
            NVector(-2, 0),  # LEFT
            NVector(-1, -1)  # UP LEFT
        ]

    def is_one_hex_move(self):
        """
        Checks if the vector points to a hexagonal field that is a direct neighbor.

        :return: True if the vector is a one hex move, false otherwise.
        """
        return abs(self.d_x) == abs(self.d_y) or (self.d_x % 2 == 0 and self.d_y == 0)

    def __repr__(self) -> str:
        """
        Returns the string representation of the vector.

        :return: The string representation of the vector.
        """
        return f"NVector({self.d_x}, {self.d_y})"

    def __eq__(self, other):
        """
        Overrides the default equality operator to check if two NVector objects are equal.

        :param other: The other NVector object to compare to.
        :return: True if the two NVector objects are equal, False otherwise.
        """
        if isinstance(other, NVector):
            return self.d_x == other.d_x and self.d_y == other.d_y
        return False


class NCoordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def to_vector(self) -> NVector:
        """
        Converts the coordinate to a vector.
        """
        return NVector(d_x=self.x, d_y=self.y)

    def distance(self, other: 'NCoordinate') -> float:
        """
        Calculates the distance between two coordinates.

        :param other: The other coordinate to calculate the distance to.
        :return: The distance between the two cartesian coordinates.
        """
        return self.to_vector().subtraction(other.to_vector()).magnitude()

    def add_vector(self, vector: NVector) -> 'NHexCoordinate':
        """
        Adds a vector to the hex coordinate.

        :param vector: The vector to add.
        :return: The new hex coordinate.
        """
        vector: NVector = self.to_vector().addition(vector)
        return NHexCoordinate(x=vector.d_x, y=vector.d_y)

    def subtract_vector(self, vector: NVector) -> 'NHexCoordinate':
        """
        Subtracts a vector from the hex coordinate.

        :param vector: The vector to subtract.
        :return: The new hex coordinate.
        """
        vector: NVector = self.to_vector().subtraction(vector)
        return NHexCoordinate(x=vector.d_x, y=vector.d_y)


class NCartesianCoordinate(NCoordinate):
    """
    Represents a coordinate in a normal cartesian coordinate system, that has been taught in school.
    This class is used to translate and represent a hexagonal coordinate in a cartesian and with that a 2D-Array.
    """

    def is_inbounce(self):
        return 0<=self.x<=7 and 0<=self.y<=7

    def add_vector(self, vector: NVector) -> 'NCartesianCoordinate':
        """
        Adds a vector to the cartesian coordinate.

        :param vector: The vector to add.
        :return: The new cartesian coordinate.
        """
        vector: NVector = self.to_vector().addition(vector)
        return NCartesianCoordinate(x=vector.d_x, y=vector.d_y)

    def subtract_vector(self, vector: NVector) -> 'NCartesianCoordinate':
        """
        Subtracts a vector from the cartesian coordinate.

        :param vector: The vector to subtract.
        :return: The new cartesian coordinate.
        """
        vector: NVector = self.to_vector().subtraction(vector)
        return NCartesianCoordinate(x=vector.d_x, y=vector.d_y)

    def to_hex(self) -> 'NHexCoordinate':
        """
        Converts the cartesian coordinate to a hex coordinate.

        :return: The hex coordinate.
        """
        return NHexCoordinate(x= (self.x<<1) + (1 if self.y % 2 == 1 else 0), y=self.y)

    def to_index(self) -> Optional[int]:
        """
        Converts the cartesian coordinate to an index.

        :return: The index or None if the coordinate is not valid.
        """
        if self.is_inbounce():
            return self.y * 8 + self.x
        return None

    @staticmethod
    def from_index(index: int, width: int, height: int) -> Optional['NCartesianCoordinate']:
        """
        Converts a given index to a NCartesianCoordinate.

        Args:
            index: The index to convert.
            width: The width of the grid.
            height: The height of the grid.

        Returns:
            Optional[NCartesianCoordinate]: The NCartesianCoordinate that corresponds to the given index, or None if the
            index is out of range.
        """
        if index < 0 or index >= width * height:
            raise IndexError(f"Index out of range. The index has to be 0 <= {index} < {width * height}")
        x = index % width
        y = index // width
        return NCartesianCoordinate(x, y)

    def __repr__(self) -> str:
        return f"NCartesianCoordinate({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NCartesianCoordinate) and self.x == other.x and self.y == other.y


class NHexCoordinate(NCoordinate):
    """
    Represents a coordinate in a hexagonal coordinate system, that differs from the normal cartesian one.
    This class is used to represent the hexagonal game board.
    """

    def is_inbounce(self):
        cartesian = self.to_cartesian()
        return cartesian.is_inbounce()

    def to_cartesian(self) -> NCartesianCoordinate:
        """
        Converts the hex coordinate to a cartesian coordinate.

        :return: The cartesian coordinate.
        """
        return NCartesianCoordinate(x= self.x>>1, y=self.y)

    def add_vector(self, vector: NVector) -> 'NHexCoordinate':
        """
        Adds a vector to the hex coordinate.

        :param vector: The vector to add.
        :return: The new hex coordinate.
        """
        vector: NVector = self.to_vector().addition(vector)
        return NHexCoordinate(x=vector.d_x, y=vector.d_y)

    def subtract_vector(self, vector: NVector) -> 'NHexCoordinate':
        """
        Subtracts a vector from the hex coordinate.

        :param vector: The vector to subtract.
        :return: The new hex coordinate.
        """
        vector: NVector = self.to_vector().subtraction(vector)
        return NHexCoordinate(x=vector.d_x, y=vector.d_y)

    def get_neighbors(self) -> List['NHexCoordinate']:
        """
        Returns a list of all neighbors of the hex coordinate.

        :return: The list of neighbors.
        """
        return [self.add_vector(vector) for vector in self.to_vector().directions]

    def __repr__(self) -> str:
        return f"NHexCoordinate({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NHexCoordinate) and self.x == other.x and self.y == other.y