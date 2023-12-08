from common import CodeBase


class ScratchCard:
    def __init__(self, line):
        content_tokens = line.split(":")[1].split("|")
        self.winning_numbers = [int(token.strip()) for token in content_tokens[0].split()]
        self.owned_numbers = [int(token.strip()) for token in content_tokens[1].split()]

    def get_n_matches(self):
        return len(set(self.winning_numbers) & set(self.owned_numbers))

    def get_worth(self):
        n_matches = self.get_n_matches()
        score = 0 if n_matches == 0 else 2 ** (n_matches - 1)
        return score


class Code(CodeBase):

    def __init__(self):
        super().__init__("D4")

    def run(self):
        self.greet()
        n_copies = [1 for _ in range(len(self.lines))]
        s = 0
        for i, line in enumerate(self.lines):
            scratch_card = ScratchCard(line)
            s += scratch_card.get_worth()
            n_matches = scratch_card.get_n_matches()
            for j in range(i + 1, i + 1 + n_matches):
                n_copies[j] += n_copies[i]

        print(f"Total winnings: {s}")
        print(f"Number of copies: {sum(n_copies)}")
