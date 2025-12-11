def multisets_permutations(counts, prefix, remaining, out):
    """
    Efficient permutation generator for multisets.
    counts: dict of number -> count
    prefix: current building permutation
    remaining: how many elements still need to be placed
    out: output function or collector
    """
    if remaining == 0:
        out(tuple(prefix))
        return

    for value in list(counts.keys()):
        if counts[value] > 0:
            counts[value] -= 1
            prefix.append(value)
            multisets_permutations(counts, prefix, remaining - 1, out)
            prefix.pop()
            counts[value] += 1


def moves(s):
    """
    Generate all unique lists of size s with elements 0..s
    whose SORTED version satisfies:
        1. adjacent diffs <= 2
        2. sorted[0] <= 1
        3. sorted[-1] >= s - 1
    """

    # Recursive generator of sorted lists meeting the adjacency rule.
    # We generate only VALID sorted lists.
    def build_sorted(prev, length):
        if length == s:
            # Check endpoint conditions only once fully built
            if prev[0] <= 1 and prev[-1] >= s - 1:
                yield prev
            return

        last = prev[-1]
        # Next value can be last, last+1, last+2 (bounded by 0..s)
        for nxt in (last, last+1, last+2):
            if 0 <= nxt < s:
                yield from build_sorted(prev + (nxt,), length + 1)

    # Kick off sorted generation with allowed starting values
    for start in (0, 1):
        for sorted_list in build_sorted((start,), 1):

            # Convert sorted_list into multiset counts
            counts = {}
            for v in sorted_list:
                counts[v] = counts.get(v, 0) + 1

            # Instead of returning a huge list, we yield through a buffer
            results = []
            multisets_permutations(counts, [], s, results.append)

            for r in results:
                yield r


# ---------- Example usage ----------
if __name__ == "__main__":
    s = 6
    for lst in moves(s):
        print(lst)
