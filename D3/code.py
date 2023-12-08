import regex as re
from typing import Iterator

from common import CodeBase


class Code(CodeBase):
    def __init__(self):
        super().__init__("D3")
        self.symbols = ["&", "*", "$", "-", "%", "@", "+", "/", "#", "="]
        # Construct a regex that matches any of the symbols in the list above, escape special characters
        self.symbols_regex = re.compile(r"[" + re.escape("".join(self.symbols)) + "]")
        self.digits_regex = re.compile(r"\d+")
        self.gear_regex = re.compile(re.escape("*"))
        self.line_length = 0
        self.n_lines = 0

    def run(self):
        self.greet()

        self.n_lines = len(self.lines)

        s = 0
        gear_links = {}
        for i, line in enumerate(self.lines):
            if self.line_length == 0:
                self.line_length = len(line)
            part_spans = self.get_part_spans(line)
            for part_span in part_spans:
                adjacent_cells = self.get_adjacent_cells(part_span, i)
                if self.has_adjacent_symbols(adjacent_cells):
                    part_number = int(line[part_span[0]:part_span[1]])
                    s += part_number
                    gears = self.get_adjacent_gears(adjacent_cells)
                    for gear in gears:
                        gear_id = self.get_gear_id(gear, part_span, i)
                        if gear_id not in gear_links:
                            gear_links[gear_id] = []
                        gear_links[gear_id].append(part_number)

        gear_ratios = 0
        for gear_id, part_numbers in gear_links.items():
            if len(part_numbers) == 2:
                gear_ratios += part_numbers[0] * part_numbers[1]
        print("The sum is: ", s)
        print("The gear ratios sum is: ", gear_ratios)

    def get_part_spans(self, line):
        parts: Iterator[re.Match] = self.digits_regex.finditer(line)
        return [part.span() for part in parts]

    def get_adjacent_cells(self, part_span, i):
        adjacent_cells = ""
        start = part_span[0] - 1 if part_span[0] > 0 else 0
        end = part_span[1] + 1 if part_span[1] < len(self.lines[i]) else len(self.lines[i])
        if i > 0:
            adjacent_cells += self.lines[i - 1][start:end]
        if start < part_span[0]:
            adjacent_cells += self.lines[i][start:start + 1]
        if end > part_span[1]:
            adjacent_cells += self.lines[i][end - 1:end]
        if i < self.n_lines - 1:
            adjacent_cells += self.lines[i + 1][start:end]
        return adjacent_cells

    def has_adjacent_symbols(self, adjacent_cells):
        return self.symbols_regex.search(adjacent_cells) is not None

    def get_adjacent_gears(self, adjacent_cells):
        gears: Iterator[re.Match] = self.gear_regex.finditer(adjacent_cells)
        return [p.span()[0] for p in gears]

    def get_gear_id(self, gear, part_span, i):
        start = part_span[0] - 1 if part_span[0] > 0 else 0
        end = part_span[1] + 1 if part_span[1] < self.line_length else self.line_length
        rows = []
        cols = []
        if i > 0:
            rows += [i - 1 for _ in range(start, end)]
            cols += [j for j in range(start, end)]
        if start < part_span[0]:
            rows.append(i)
            cols.append(start)
        if end > part_span[1]:
            rows.append(i)
            cols.append(end-1)
        if i < self.n_lines - 1:
            rows += [i + 1 for _ in range(start, end)]
            cols += [j for j in range(start, end)]
        # print('---------------->')
        # print(part_span, i)
        # print(start, end)
        # print(rows, cols, gear)
        # print('----------------<')
        if gear >= len(rows):
            print('---------------->')
            print(part_span, i)
            print(start, end)
            print(rows, cols, gear)
            print('----------------<')
        gear_row = rows[gear]
        gear_col = cols[gear]
        return 1000 * gear_row + gear_col


def test():
    code = Code()
    patterns = [
        "$....787..80..",
        "...639.&.541..",
        "...*....644*..",
        ".*22$...*..*..",
        "115...312.213.",
        "32...........*",
        "..*..........."
    ]
    code.line_length = len(patterns[0])
    code.n_lines = len(patterns)
    print(code.symbols_regex)
    for i, pattern in enumerate(patterns):
        part_spans = code.get_part_spans(pattern)
        print(f"Pattern: {pattern}")
        print(f" - {part_spans}")
        for part_span in part_spans:
            adjacent_cells = code.get_adjacent_cells(part_span, patterns, i)
            gears = code.get_adjacent_gears(adjacent_cells)
            print(f"   - {pattern[part_span[0]:part_span[1]]}")
            print(f"     - {adjacent_cells}")
            print(f"     - {code.has_adjacent_symbols(adjacent_cells)}")
            print(f"     - {gears}")
            for gear in gears:
                gear_id = code.get_gear_id(gear, part_span, i)
                print(f"       - {gear_id}")
        print()


if __name__ == '__main__':
    test()
