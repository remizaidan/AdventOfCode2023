
from common import CodeBase


class Range:
    def __init__(self, source_start, target_start, length):
        self.source_start = source_start
        self.target_start = target_start
        self.length = length

    def contains(self, source_value):
        return self.source_start <= source_value < self.source_start + self.length

    def map_value(self, source_value):
        return self.target_start + (source_value - self.source_start)

    def reverse_map_value(self, target_value):
        return self.source_start + (target_value - self.target_start)

    def get_intersection(self, other_start, other_length):
        self_start = self.target_start
        self_end = self.target_start + self.length - 1
        other_end = other_start + other_length - 1
        return max(self_start, other_start), min(self_end, other_end)

    def __str__(self):
        return (
            f'{self.source_start}:{self.source_start+self.length-1}'
            f' -> '
            f'{self.target_start}:{self.target_start+self.length-1}'
        )


class Map:
    def __init__(self):
        self.ranges = []
        self.updated_ranges = []

    def add_source_range(self, source_start, length):
        self.ranges.append(Range(source_start, source_start, length))
        self.updated_ranges.append(False)

    def map_value(self, source_value):
        for r in self.ranges:
            if r.contains(source_value):
                return r.map_value(source_value)
        return source_value

    def update_range(self, old_target_start, update_target_start, length):
        update_range = Range(old_target_start, update_target_start, length)
        new_ranges = []
        new_updated_ranges = []
        for i_r, r in enumerate(self.ranges):
            if self.updated_ranges[i_r]:
                new_ranges.append(r)
                new_updated_ranges.append(True)
                continue
            intersection = r.get_intersection(old_target_start, length)
            if intersection[0] > intersection[1]:
                new_ranges.append(r)
                new_updated_ranges.append(self.updated_ranges[i_r])
                continue
            if r.target_start < intersection[0]:
                new_source_start = r.source_start
                new_target_start = r.target_start
                new_length = intersection[0] - r.target_start
                new_ranges.append(Range(new_source_start, new_target_start, new_length))
                new_updated_ranges.append(False)
            new_source_start = r.reverse_map_value(intersection[0])
            new_target_start = update_range.map_value(intersection[0])
            new_length = intersection[1] - intersection[0] + 1
            new_ranges.append(Range(new_source_start, new_target_start, new_length))
            new_updated_ranges.append(True)
            if r.target_start + r.length - 1 > intersection[1]:
                new_source_start = r.reverse_map_value(intersection[1]+1)
                new_target_start = intersection[1] + 1
                new_length = r.target_start + r.length - new_target_start
                new_ranges.append(Range(new_source_start, new_target_start, new_length))
                new_updated_ranges.append(False)
        self.ranges = new_ranges
        self.updated_ranges = new_updated_ranges

    def reset_updates(self):
        self.updated_ranges = [False] * len(self.ranges)

    def __str__(self):
        return str([str(r) for r in self.ranges])


class Code(CodeBase):

    def __init__(self):
        super().__init__("D5")
        self.seeds = []
        self.seeds_map = Map()
        self.extended_seeds_map = Map()
        self.current_source = None
        self.current_target = None

    def run(self):
        self.greet()

        for line in self.lines:
            self.process_line(line)

        self.print_best_location("seeds", self.seeds_map)
        self.print_best_location("extended seeds", self.extended_seeds_map)

    def process_line(self, line):
        if line.startswith("seeds"):
            self.process_seeds(line)
        elif "map:" in line:
            self.init_new_map(line)
        elif line.strip() != "":
            self.process_map(line)

    def process_seeds(self, line):
        self.seeds = [int(token.strip()) for token in line.split(":")[1].split()]
        for seed in self.seeds:
            self.seeds_map.add_source_range(seed, 1)
        for i in range(len(self.seeds) // 2):
            seed = self.seeds[2 * i]
            length = self.seeds[2 * i + 1]
            self.extended_seeds_map.add_source_range(seed, length)

    def init_new_map(self, line):
        map_tokens = line.replace("map:", "").strip().split("-")
        source = map_tokens[0].strip()
        target = map_tokens[-1].strip()
        self.current_source = source
        self.current_target = target
        self.seeds_map.reset_updates()
        self.extended_seeds_map.reset_updates()

    def process_map(self, line):
        target_start, source_start, length = [int(l.strip()) for l in line.split()]
        self.seeds_map.update_range(source_start, target_start, length)
        self.extended_seeds_map.update_range(source_start, target_start, length)

    @staticmethod
    def print_best_location(name, seeds_map):
        locations = [seeds_map.map_value(r.source_start) for r in seeds_map.ranges]
        print(f'Best {name} location: {min(locations)}')


def test():

    lines = [
        "seeds: 79 14 55 13",
        "",
        "seed-to-soil map:",
        "50 98 2",
        "52 50 48",
        "",
        "soil-to-fertilizer map:",
        "0 15 37",
        "37 52 2",
        "39 0 15",
        "",
        "fertilizer-to-water map:",
        "49 53 8",
        "0 11 42",
        "42 0 7",
        "57 7 4",
        "",
        "water-to-light map:",
        "88 18 7",
        "18 25 70",
        "",
        "light-to-temperature map:",
        "45 77 23",
        "81 45 19",
        "68 64 13",
        "",
        "temperature-to-humidity map:",
        "0 69 1",
        "1 0 69",
        "",
        "humidity-to-location map:",
        "60 56 37",
        "56 93 4",
    ]
    code = Code()

    prev_source = None
    prev_target = None
    for i, line in enumerate(lines):
        code.process_line(line)
        if i == 0:
            print(code.seeds)
            print(">>>> Original seeds map:")
            print(code.seeds_map)
            print(code.extended_seeds_map)
        if code.current_target != prev_target:
            if prev_target is not None:
                print(f"================= {prev_source} -> {prev_target} ===================")
                print(code.seeds_map)
                print(code.extended_seeds_map)
            prev_source = code.current_source
            prev_target = code.current_target
    print(f"================= {code.current_source} -> {code.current_target} ===================")
    print(code.seeds_map)
    print(code.extended_seeds_map)

    code.print_best_location("seeds", code.seeds_map)
    code.print_best_location("extended seeds", code.extended_seeds_map)


if __name__ == '__main__':
    test()
