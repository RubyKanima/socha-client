from socha import Field

from dataclasses import dataclass

@dataclass
class Triangle:
    root: Field
    left: Field
    right: Field
    orient: int # 1 or -1

    @property
    def fish(self):
        return sum(self.root.fish, self.left.fish, self.right.fish)
     


