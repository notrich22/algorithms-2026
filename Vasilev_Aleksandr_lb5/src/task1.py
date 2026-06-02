ALPHABET = "ACGTN"

ID = {
    "A": 0,
    "C": 1,
    "G": 2,
    "T": 3,
    "N": 4
}


class Node:
    def __init__(self):
        self.next = [-1] * 5
        self.link = 0
        self.term = -1
        self.out = []


class AhoCorasick:
    def __init__(self):
        self.nodes = [Node()]

    def add_pattern(self, pattern, pattern_id):
        print(f"добавление образца {pattern_id}: {pattern}")

        v = 0

        for ch in pattern:
            c = ID[ch]

            if self.nodes[v].next[c] == -1:
                new_v = len(self.nodes)
                self.nodes[v].next[c] = new_v
                self.nodes.append(Node())

                print(f"  новое ребро: {v} --{ch}--> {new_v}")
            else:
                print(f"  старое ребро: {v} --{ch}--> {self.nodes[v].next[c]}")

            v = self.nodes[v].next[c]

        self.nodes[v].out.append(pattern_id)
        print(f"  out[{v}] = {self.nodes[v].out}")

    def build(self):
        print("\nпостроение автомата")

        queue = []
        head = 0

        print("корень:")

        for c in range(5):
            u = self.nodes[0].next[c]

            if u == -1:
                self.nodes[0].next[c] = 0
            else:
                self.nodes[u].link = 0
                queue.append(u)

            print(f"  {ALPHABET[c]} -> {self.nodes[0].next[c]}")

        while head < len(queue):
            v = queue[head]
            head += 1

            print(f"вершина {v}")

            for c in range(5):
                u = self.nodes[v].next[c]

                if u == -1:
                    self.nodes[v].next[c] = self.nodes[self.nodes[v].link].next[c]
                else:
                    self.nodes[u].link = self.nodes[self.nodes[v].link].next[c]

                    suffix = self.nodes[u].link

                    if self.nodes[suffix].out:
                        self.nodes[u].term = suffix
                    else:
                        self.nodes[u].term = self.nodes[suffix].term

                    print(
                        f"  ребро {v} --{ALPHABET[c]}--> {u}; "
                        f"link[{u}] = {self.nodes[u].link}; "
                        f"term[{u}] = {self.nodes[u].term}"
                    )

                    queue.append(u)

    def print_automaton(self):
        print("\nавтомат")

        for i in range(len(self.nodes)):
            print(f"вершина {i}")

            for c in range(5):
                print(f"  {ALPHABET[c]} -> {self.nodes[i].next[c]}")

            print(f"  link = {self.nodes[i].link}")
            print(f"  term = {self.nodes[i].term}")
            print(f"  out = {self.nodes[i].out}")

    def find_all(self, text):
        print("\nпоиск")

        v = 0

        for i in range(len(text)):
            ch = text[i]
            c = ID[ch]

            old_v = v
            v = self.nodes[v].next[c]

            print(f"позиция {i + 1}, символ {ch}: {old_v} -> {v}")

            u = v

            while u != -1:
                for pattern_id in self.nodes[u].out:
                    print(f"  найден образец {pattern_id}, конец = {i + 1}")
                    yield i, pattern_id

                u = self.nodes[u].term


def main():
    text = input().strip()
    n = int(input())

    aho = AhoCorasick()
    lengths = [0] * (n + 1)

    print("входные данные")
    print(f"text = {text}")
    print(f"n = {n}")

    print("\nбор")

    for pattern_id in range(1, n + 1):
        pattern = input().strip()
        lengths[pattern_id] = len(pattern)
        aho.add_pattern(pattern, pattern_id)

    aho.build()
    aho.print_automaton()

    answer = [[] for _ in range(len(text))]

    for end_pos, pattern_id in aho.find_all(text):
        start_pos = end_pos - lengths[pattern_id] + 1

        print(
            f"  начало образца {pattern_id}: "
            f"{end_pos + 1} - {lengths[pattern_id]} + 1 = {start_pos + 1}"
        )

        if start_pos >= 0:
            answer[start_pos].append(pattern_id)

    print("\nответ")

    for pos in range(len(text)):
        answer[pos].sort()

        for pattern_id in answer[pos]:
            print(pos + 1, pattern_id)


main()