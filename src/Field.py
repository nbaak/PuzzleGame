

class Field:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = None
        self.create_new_field()

    def create_new_field(self):
        self.field = [[0 for _ in range(self.width)] for _ in range(self.height)]
        return self.field

    def show(self):
        if self.field:
            for line in self.field:
                print(line)
        else:
            print("no field!")

    def place_at(self, item, pos:tuple[int], override=False):
        if pos[0] < 0 or pos[0] >= self.width:
            return None
        if pos[1] < 0 or pos[1] >= self.height:
            return None
        
        if self.field[pos[1]][pos[0]] == 0 or override:
            self.field[pos[1]][pos[0]] = item

    def get_at(self, pos:tuple[int]):
        if pos[0] < 0 or pos[0] >= self.width:
            return None
        if pos[1] < 0 or pos[1] >= self.height:
            return None
        return self.field[pos[1]][pos[0]]


if __name__ == "__main__":
    field = Field(5, 5)

    # field.place_at(1, (2, 0))
    # field.place_at(1, (2, 1))

    field.place_at(2, (2, 3))
    field.place_at(2, (2, 4))

    # field.place_at(1, (0, 2))
    # field.place_at(1, (1, 2))

    field.place_at(1, (3, 2))
    field.place_at(1, (4, 2))

    field.place_at(1, (2, 2))

    field.place_at(1, (0, 0))

    field.show()

