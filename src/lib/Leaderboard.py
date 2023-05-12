
from pathlib import Path
import os


class Leaderboard:

    def __init__(self, width, height, level, file_location="./"):

        if Path(file_location).exists():
            self.file_location = Path(file_location)
        else:
            Path(file_location).mkdir(parents=True)
            self.file_location = Path(file_location)

        self.width = width
        self.height = height
        self.level = level

        self.filename = Path(self.file_location, f"{width}-{height}-{level}.ladder")

        self.ladder = []

        self.load()

    def add_user(self, user:str, session:str, points:int):

        def get_values(iterables, key_to_find):
            return list(filter(lambda x:key_to_find in x, iterables))

        if not get_values(self.ladder, session):
            self.ladder.append((user, session, points))
            self.ladder.sort(key=lambda x: x[2], reverse=True)
            self.save()

    def __write_to_file(self):
        with open(self.filename, 'w') as f:
            for user, session, points in self.ladder:
                line = f"{user},{session},{points}\n"
                f.write(line)

    def save(self):
        return self.__write_to_file()

    def load(self):
        if Path(self.filename).exists():
            with open(self.filename, 'r') as f:
                data = f.read().strip().split('\n')

                # maybe there is a nicer way?
                self.ladder = [tuple([line.split(',')[0], line.split(',')[1], int(line.split(',')[2])]) for line in data if line]

    def show(self):
        ladder = ""
        for user, session, points in self.ladder:
            ladder += f"{user} - {session} - {points}\n"

        print(ladder)

    def get(self):
        return [(nr, data[0], data[1], data[2]) for nr, data in enumerate(self.ladder)]

    def __repr__(self):
        return f'{self.ladder[0]} {len(self.ladder)}'

    @staticmethod
    def load_leaderboards(path:str):
        if Path(path).exists():
            boards = {}
            for file in os.listdir(path):
                if file.endswith(".ladder"):
                    print('loading', file)
                    board, _ = file.split('.')
                    w, h, l = board.split('-')
                    boards[board] = Leaderboard(w, h, l, path)

            return boards

        return None


if __name__ == "__main__":
    l = Leaderboard(4, 3, 1)
    l.add_user("A", "sA", 10)
    l.add_user("B", "sB", 20)
    l.add_user("C", "sC", 5)
    l.add_user("D", "sD", 100)
    l.add_user("D", "sD", 100)
    l.add_user("D", "sD", 100)
    l.add_user("D", "sD", 100)

    l.add_user("X", "sX", 10000)

    l.show()
    l.save()
    print(l)
    print("save location:")
    print(l.filename.resolve())
    print(l.get())

    Leaderboard.load_leaderboards('.')

