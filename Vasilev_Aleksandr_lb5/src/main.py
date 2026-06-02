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

    def print_automaton(self, names):
        print("\nавтомат")

        for i in range(len(self.nodes)):
            print(f"вершина {i} ({names[i]})")

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

    def get_trie_info(self):
        names = [""] * len(self.nodes)
        names[0] = "ε"

        trie_edges = []

        stack = [0]

        while stack:
            v = stack.pop()

            for c in range(5):
                u = self.nodes[v].next[c]

                if u != -1:
                    trie_edges.append((v, u, ALPHABET[c]))

                    if v == 0:
                        names[u] = ALPHABET[c]
                    else:
                        names[u] = names[v] + ALPHABET[c]

                    stack.append(u)

        return names, trie_edges
    
    def write_dot(self, names, trie_edges=None, filename="automaton.dot", mode="compact"):
        f = open(filename, "w", encoding="utf-8")

        f.write("digraph AhoCorasick {\n")
        f.write("    rankdir=LR;\n")
        f.write("    graph [nodesep=0.8, ranksep=1.2];\n")
        f.write("    node [shape=circle];\n")
        f.write("    edge [fontsize=10];\n\n")

        for i in range(len(self.nodes)):
            label = f"{i}\\n{names[i]}"

            if self.nodes[i].out:
                label += "\\nout=" + ",".join(map(str, self.nodes[i].out))
                f.write(f'    {i} [label="{label}", shape=doublecircle];\n')
            else:
                f.write(f'    {i} [label="{label}"];\n')

        f.write("\n")

        levels = {}

        for i in range(len(names)):
            if names[i] == "ε":
                depth = 0
            else:
                depth = len(names[i])

            if depth not in levels:
                levels[depth] = []

            levels[depth].append(i)

        for depth in sorted(levels):
            vertices = " ".join(map(str, levels[depth]))
            f.write(f"    {{ rank=same; {vertices}; }}\n")

        f.write("\n")

        if mode == "compact":
            for v, u, ch in trie_edges:
                f.write(f'    {v} -> {u} [label="{ch}"];\n')

            f.write("\n")

            for i in range(1, len(self.nodes)):
                f.write(
                    f'    {i} -> {self.nodes[i].link} '
                    f'[label="suf", style=dashed, constraint=false];\n'
                )

            f.write("\n")

            for i in range(len(self.nodes)):
                term = self.nodes[i].term

                if term != -1:
                    f.write(
                        f'    {i} -> {term} '
                        f'[label="term", style=dotted, constraint=false];\n'
                    )

        elif mode == "full":
            for i in range(len(self.nodes)):
                for c in range(5):
                    to = self.nodes[i].next[c]
                    f.write(f'    {i} -> {to} [label="{ALPHABET[c]}"];\n')

        f.write("}\n")
        f.close()

        print(f"\nграф записан в файл {filename}")

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

    names, trie_edges = aho.get_trie_info()

    aho.build()
    aho.print_automaton(names)

    aho.write_dot(names, trie_edges, "automaton.dot")
    aho.write_dot(names, filename="automaton_full.dot", mode="full")

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

    found = False

    for pos in range(len(text)):
        answer[pos].sort()

        for pattern_id in answer[pos]:
            found = True
            print(pos + 1, pattern_id)

    if not found:
        print("вхождений нет")


main()