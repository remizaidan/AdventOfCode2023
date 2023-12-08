from common import CodeBase


class Code(CodeBase):
    def __init__(self):
        super().__init__("D2")
        self.max_red = 12
        self.max_green = 13
        self.max_blue = 14

    def run(self):
        self.greet()

        s = 0
        s_power = 0
        for line in self.lines:
            game_id, is_possible, game_power = self.examine_game(line)

            if is_possible:
                s += game_id
            s_power += game_power

        print("The sum is: ", s)
        print("The sum of powers is: ", s_power)

    def examine_game(self, line):
        game_id, game_content = self.parse_line(line)
        game_sets = self.parse_game(game_content)

        is_possible = True
        r_needed, g_needed, b_needed = 0, 0, 0
        for game_set in game_sets:
            r, g, b = self.parse_set(game_set)
            if r > self.max_red or g > self.max_green or b > self.max_blue:
                is_possible = False
            if r > r_needed:
                r_needed = r
            if g > g_needed:
                g_needed = g
            if b > b_needed:
                b_needed = b

        game_power = r_needed * g_needed * b_needed

        return game_id, is_possible, game_power

    @staticmethod
    def parse_line(line):
        tokens = line.split(":")
        if len(tokens) != 2:
            raise Exception(f"Invalid line: {line}")

        game_id = int(tokens[0].replace('Game ', ''))
        game_content = tokens[1]

        return game_id, game_content

    @staticmethod
    def parse_game(game_content):
        tokens = game_content.split(";")
        return tokens

    @staticmethod
    def parse_set(game_set):
        groups = game_set.split(",")
        r, g, b = 0, 0, 0
        for group in groups:
            if "red" in group:
                r = int(group.replace('red', '').strip())
            elif "green" in group:
                g = int(group.replace('green', '').strip())
            elif "blue" in group:
                b = int(group.replace('blue', '').strip())
            else:
                raise Exception(f"Invalid group: {group}")
        return r, g, b


def test():
    line = "Game 1: 1 red, 2 green, 3 blue;4 blue, 5 red"
    code = Code()
    game_id, game_content = code.parse_line(line)
    game_sets = code.parse_game(game_content)
    print(f"Game id: {game_id}")
    print(f"Game sets: {len(game_sets)}")
    for game_set in game_sets:
        r, g, b = code.parse_set(game_set)
        print(f" - {r} red, {g} green, {b} blue")


if __name__ == '__main__':
    test()
