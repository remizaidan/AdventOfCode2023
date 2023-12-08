import numpy as np
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


class Map:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.ranges = []

    def add_range(self, source_start, target_start, length):
        self.ranges.append(Range(source_start, target_start, length))
        self.ranges.sort(key=lambda r: r.source_start)

    def map_value(self, source_value):
        for r in self.ranges:
            if r.contains(source_value):
                return r.map_value(source_value)
        return source_value


class Code(CodeBase):

    def __init__(self):
        super().__init__("D5")
        self.seeds = []
        self.extended_seeds = []
        self.seed_ranges = []
        self.current_map = None
        self.map_of_maps = {}

    def run(self):
        self.greet()

        for line in self.lines:
            self.process_line(line)

        self.compute_extended_seeds()

        locations = [self.follow_seed(seed)[0] for seed in self.seeds]
        print(f'Best location: {min(locations)}')

        extended_locations = [self.follow_seed(seed)[0] for seed in self.extended_seeds]
        print(f'Best extended location: {min(extended_locations)}')

    def process_line(self, line):
        if line.startswith("seeds"):
            self.process_seeds(line)
        elif "map:" in line:
            self.init_new_map(line)
        elif line.strip() != "":
            self.process_map(line)

    def process_seeds(self, line):
        self.seeds = [int(token.strip()) for token in line.split(":")[1].split()]
        self.extended_seeds = []
        for i in range(len(self.seeds)//2):
            seed = self.seeds[2*i]
            length = self.seeds[2*i+1]
            self.seed_ranges.append((seed, length))
            self.seed_ranges.sort(key=lambda r: r[0])

    def init_new_map(self, line):
        map_tokens = line.replace("map:", "").strip().split("-")
        source = map_tokens[0].strip()
        target = map_tokens[-1].strip()
        self.current_map = source
        self.map_of_maps[source] = Map(source, target)

    def process_map(self, line):
        target_start, source_start, length = [int(l.strip()) for l in line.split()]
        self.map_of_maps[self.current_map].add_range(source_start, target_start, length)

    def follow_seed(self, seed):
        source = "seed"
        target = None
        while source in self.map_of_maps:
            target = self.map_of_maps[source].target
            seed = self.map_of_maps[source].map_value(seed)
            source = target
        return seed, target

    def compute_extended_seeds(self):
        map_source = "seed"
        while map_source in self.map_of_maps:
            self.update_seed_ranges(map_source)
            map_source = self.map_of_maps[map_source].target

        self.extended_seeds = [r[0] for r in self.seed_ranges]

    def update_seed_ranges(self, map_source):
        m = self.map_of_maps[map_source]
        seed_edges = np.array(self.seed_ranges)
        seed_edges[:, 1] = seed_edges[:, 0] + seed_edges[:, 1]
        seed_edges = np.unique(np.sort(seed_edges.flatten()))
        map_edges = np.array(
            [r.source_start for r in m.ranges] +
            [r.source_start + r.length for r in m.ranges]
        )
        map_edges = np.unique(np.sort(map_edges))
        new_edges = np.unique(np.sort(np.concatenate((seed_edges, map_edges))))
        new_ranges = np.hstack((new_edges[:-1].reshape(-1, 1), np.diff(new_edges).reshape(-1, 1)))
        self.seed_ranges = [(r[0], r[1]) for r in new_ranges]


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

    for line in lines:
        code.process_line(line)
    print(code.seeds)
    for key, value in code.map_of_maps.items():
        print(f'{key}: {value.source} -> {value.target}')
    for seed in code.seeds:
        print(f'{seed} -> {code.follow_seed(seed)}')

    print(code.seed_ranges)
    code.compute_extended_seeds()
    print(code.seed_ranges)
    print(code.extended_seeds)


if __name__ == '__main__':
    test()
