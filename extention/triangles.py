from socha import Field

from dataclasses import dataclass, field

@dataclass(eq=False, order=True) # adds __eq__ function
class Triangle:
    root: Field
    left: Field
    right: Field
    orient: int = field(default=1)

    @property
    def fish(self):
        return sum(self.root.fish, self.left.fish, self.right.fish)
     
