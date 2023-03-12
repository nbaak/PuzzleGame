from Field import Field
import random


class Game(Field):

    def __init__(self, width, height, level=0):
        super().__init__(width, height)
        self.level = level
        self.max_value = 1

        self._create_queue()

        self.blocked_fields = set()
        self._generate_obstacle()

        self.points = 0
        self.step = 0

    def _generate_obstacle(self):
        while len(self.blocked_fields) < self.level:
            r_pos = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            self.place_at(-1, r_pos)
            self.blocked_fields.add(r_pos)

    def _create_queue(self):
        self.queue = [random.randint(1, self.max_value) for _ in range(10)]  # maybe deque?
        return self.queue

    def check_rules(self, pos:tuple[int], check_value:int, found:list=None, skip=False) -> tuple[int, bool]:
        if not type(check_value) is int:
            return 0

        pos_value = self.get_at(pos)
        if pos_value == -1:
            return 0

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        def tuple_add(t1, t2):
            return (t1[0] + t2[0], t1[1] + t2[1])

        points = 0
        found = found or []
        for d in directions:
            c_pos = tuple_add(pos, d)
            if c_pos in found:
                # print(f'skip {c_pos}')
                continue

            value = self.get_at(c_pos)

            if value == pos_value:
                found.append(c_pos)
                self.check_rules(c_pos, check_value, found, True)

        # success
        if len(found) > 2 and not skip:
            points = len(found) * pos_value

            for p in found:
                self.place_at(0, p, override=True)

            self.place_at(pos_value + 1, pos)
            if pos_value + 1 > self.max_value:
                self.max_value = pos_value + 1

        gameover = self.check_possible_move()
        self.points += points
        
        return points, gameover

    def check_possible_move(self) -> bool:
        # TODO: check if there are more possible moves for the player to do. else: gameover
        for line in self.field:
            for field in line:
                if field == 0:
                    return False

        return True

    def reset(self):
        self.create_new_field()

        self.max_value = 1
        self.points = 0
        self.step = 0

        self.blocked_fields = set()

        self._generate_obstacle()
        self._create_queue()
        
    def place_at(self, item, pos:tuple[int], override=False, do_step=False):
        if do_step:
            self.step += 1
        return Field.place_at(self, item, pos, override=override)

    def get_queue(self):
        return self.queue
    
    def get_status(self):
        return f"Level: {self.level}, Round: {self.step}, Points: {self.points}"

    def take_next_queue_element(self):
        item = self.queue.pop(0)
        self.queue.append(random.randint(1, self.max_value))
        return item

    def dims(self):
        return len(self.field[0]), len(self.field)

    def __len__(self):
        return len(self.field)


if __name__ == "__main__":
    game = Game(5, 5)
    game.show()
    print(game.get_queue())
    print()

    game.place_at(1, (2, 0))
    game.place_at(1, (2, 1))

    game.place_at(2, (2, 3))
    game.place_at(2, (2, 4))

    # game.place_at(1, (0, 2))
    # game.place_at(1, (1, 2))

    game.place_at(1, (3, 2))
    game.place_at(1, (4, 2))

    game.place_at(1, (2, 2))

    game.place_at(1, (0, 0))

    game.show()
    print()
    print(game.check_rules((2, 2), 1))

    game.show()
    print()
    print(game.check_rules((2, 2), 1))

    game.show()

    print(len(game))

