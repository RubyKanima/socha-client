from socha import Field

from dataclasses import dataclass

@dataclass
class Triangle:
    root: Field
    left: Field
    right: Field
    upside: bool

    @property
    def fish(self):
        return sum(self.root.fish, self.left.fish, self.right.fish)
     
