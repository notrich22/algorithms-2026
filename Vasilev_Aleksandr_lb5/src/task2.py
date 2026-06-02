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
        print(f"добавление фрагмента {pattern_id}: {pattern}")

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
                for part_id in self.nodes[u].out:
                    print(f"  найден фрагмент {part_id}, конец = {i + 1}")
                    yield i, part_id

                u = self.nodes[u].term


def split_pattern(pattern, joker):
    parts = []
    i = 0

    print("\nразбиение шаблона")

    while i < len(pattern):
        if pattern[i] == joker:
            print(f"позиция {i + 1}: джокер")
            i += 1
            continue

        start = i
        fragment = ""

        while i < len(pattern) and pattern[i] != joker:
            fragment += pattern[i]
            i += 1

        parts.append((fragment, start))
        print(f"фрагмент {len(parts) - 1}: {fragment}, offset = {start}")

    return parts


def main():
    text = input().strip()
    pattern = input().strip()
    joker = input().strip()

    text_len = len(text)
    pattern_len = len(pattern)

    print("входные данные")
    print(f"text = {text}")
    print(f"pattern = {pattern}")
    print(f"joker = {joker}")
    print(f"text_len = {text_len}")
    print(f"pattern_len = {pattern_len}")

    if pattern_len > text_len:
        return

    parts = split_pattern(pattern, joker)

    aho = AhoCorasick()

    lengths = []
    offsets = []

    print("\nбор")

    for part_id in range(len(parts)):
        fragment, offset = parts[part_id]

        lengths.append(len(fragment))
        offsets.append(offset)

        print(f"length[{part_id}] = {lengths[part_id]}")
        print(f"offset[{part_id}] = {offsets[part_id]}")

        aho.add_pattern(fragment, part_id)

    aho.build()
    aho.print_automaton()

    count = [0] * (text_len - pattern_len + 1)

    print("\nмассив count")
    print(count)

    for end_pos, part_id in aho.find_all(text):
        fragment_start = end_pos - lengths[part_id] + 1
        full_start = fragment_start - offsets[part_id]

        print(
            f"  фрагмент {part_id}: "
            f"fragment_start = {end_pos + 1} - {lengths[part_id]} + 1 = {fragment_start + 1}"
        )

        print(
            f"  начало шаблона: "
            f"{fragment_start + 1} - {offsets[part_id]} = {full_start + 1}"
        )

        if 0 <= full_start <= text_len - pattern_len:
            count[full_start] += 1
            print(f"  count[{full_start + 1}] = {count[full_start]}")
        else:
            print("  позиция вне границ")

    need = len(parts)

    print("\nпроверка count")
    print(f"need = {need}")

    for pos in range(len(count)):
        print(f"позиция {pos + 1}: count = {count[pos]}")

    print("\nответ")

    for pos in range(len(count)):
        if count[pos] == need:
            print(pos + 1)


main()