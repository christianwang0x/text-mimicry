import random
import sys


class Mimic:
    def __init__(self, sample, seed_length):
        self.sample_text = sample
        self.seed_length = seed_length
        self.combinations = dict()
        self.output_text = ""
        self.block_length = 1

    def get_combinations(self):
        i = 0
        sample_len = len(self.sample_text)
        while i < (sample_len-self.seed_length):
            s = self.sample_text[i:i+self.seed_length]
            if self.combinations.get(s):
                self.combinations[s] += 1
            else:
                self.combinations[s] = 1
            i += 1
        return len(self.combinations)

    def get_seed(self):
        seed = random.choice(self.combinations.keys())
        self.output_text += seed
        return seed

    def get_valid_combos(self, start_string):
        valid_combos = dict()
        suffix_len = self.block_length
        for s in self.combinations.keys():
            if s.startswith(start_string):
                newstr = s[-suffix_len:]
                if not valid_combos.get(newstr):
                    valid_combos[newstr] = self.combinations[s]
                else:
                    valid_combos[newstr] += self.combinations[s]
        return valid_combos

    def weighted_choice(self, choices):
        total = sum(w for c, w in choices.items())
        r = random.uniform(0, total)
        upto = 0
        for c, w in choices.items():
            if upto + w >= r:
                return c
            upto += w

    def generate_text(self, output_length):
        if not self.combinations:
            self.get_combinations()

        if not self.output_text:
            self.get_seed()

        start_string_len = self.seed_length - self.block_length
        while len(self.output_text) < output_length:
            start_string = self.output_text[-start_string_len:]
            valid_combos = self.get_valid_combos(start_string)
            choice = self.weighted_choice(valid_combos)
            self.output_text += choice
        return len(self.output_text)


def run():
    seed_length = 7
    output_length = 1000
    if len(sys.argv) < 2:
        print("Usage: %s sample_file [output_length] [seed_length]" % sys.argv[0])
        exit(1)
    elif len(sys.argv) == 2:
        output_length = int(sys.argv[2])
    else:
        output_length = int(sys.argv[2])
        seed_length = int(sys.argv[3])
        if seed_length < 2:
            print("Seed length must be at least 2")
            exit(1)
    sample = open(sys.argv[1]).read()
    M = Mimic(sample, seed_length)
    M.generate_text(output_length)
    print(M.output_text)

if __name__ == '__main__':
    run()

