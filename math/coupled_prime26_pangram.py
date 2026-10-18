"""Find and verify a five-pair prime pangram.

Only Python's standard library is required.
Every prime gets a unique, reversible name via coupled base-26 digits:
    a_0 = d_0
    a_j = (d_j + d_(j-1)) mod 26, for j >= 1
where digits are numbered from the units position (right to left), and
numeric symbols 0..25 are written A..Z. All base-26 digits are used,
including zero inside a numeral; there are no arbitrary word assignments.
"""

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
FULL = (1 << 26) - 1


def primes_up_to(limit):
    sieve = bytearray(b'\x01') * (limit + 1)
    sieve[:2] = b'\x00\x00'
    for p in range(2, int(limit ** .5) + 1):
        if sieve[p]:
            sieve[p*p::p] = b'\x00' * ((limit-p*p)//p+1)
    return [p for p in range(2, limit+1) if sieve[p]], sieve


def encode(n):
    if n <= 0:
        raise ValueError('Input must be positive')
    digits = []                         # Least significant first
    while n:
        digits.append(n % 26)
        n //= 26
    return ''.join(ALPHABET[(digits[j] + (digits[j-1] if j else 0)) % 26]
                   for j in range(len(digits)-1, -1, -1))


def encode_plain(n):
    if n <= 0:
        raise ValueError('Input must be positive')
    digits = []
    while n:
        digits.append(n % 26)
        n //= 26
    return ''.join(ALPHABET[d] for d in reversed(digits))


def decode(name):
    result, previous = 0, 0
    for j, character in enumerate(reversed(name)):
        coded = ALPHABET.index(character)
        digit = (coded - previous) % 26 if j else coded
        result += digit * 26**j
        previous = digit
    return result


def letter_mask(name):
    result = 0
    for character in name:
        bit = 1 << (ord(character) - ord('A'))
        if result & bit:
            return None
        result |= bit
    return result


def find_pangram(limit=5000, encoder=encode):
    primes, isprime = primes_up_to(limit)
    allowed = {}
    for p in primes:
        if p == 2:
            continue  # Cannot pair 2 with another distinct prime at even N > 4
        word = encoder(p)
        mask = letter_mask(word)
        if mask is not None:
            allowed[p] = (word, mask)

    valid_primes = sorted(allowed)
    for target in range(1360, limit+1, 2):
        pairs = []
        cover = 0
        for p in valid_primes:
            if 2*p >= target:
                break
            q = target - p
            if q not in allowed:
                continue
            word_p, mask_p = allowed[p]
            word_q, mask_q = allowed[q]
            if mask_p & mask_q:
                continue
            mask = mask_p | mask_q
            pairs.append((p, q, word_p, word_q, mask))
            cover |= mask

        if len(pairs) < 5 or cover != FULL:
            continue
        if sum(sorted((pair[4].bit_count() for pair in pairs), reverse=True)[:5]) < 26:
            continue

        by_letter = [[] for _ in range(26)]
        for i, pair in enumerate(pairs):
            for bit in range(26):
                if pair[4] & (1 << bit):
                    by_letter[bit].append(i)

        def solve(used, selected):
            if len(selected) == 5:
                return selected if used == FULL else None
            left = 5 - len(selected)
            uncovered = 26 - used.bit_count()
            if uncovered < 2*left or uncovered > 8*left:
                return None

            # Select the uncovered letter with the fewest compatible pairs.
            options = None
            for b in range(26):
                if used & (1 << b):
                    continue
                current = [i for i in by_letter[b]
                           if not pairs[i][4] & used
                           and pairs[i][4].bit_count() <= uncovered - 2*(left-1)
                           and pairs[i][4].bit_count() >= uncovered - 8*(left-1)]
                if not current:
                    return None
                if options is None or len(current) < len(options):
                    options = current
            for i in options:
                match = solve(used | pairs[i][4], selected + [i])
                if match is not None:
                    return match
            return None

        selected = solve(0, [])
        if selected is not None:
            return target, [pairs[i] for i in selected]
    return None


def verify(result, encoder=encode):
    target, pairs = result
    primes, isprime = primes_up_to(target)
    words = []
    for p, q, word_p, word_q, _ in pairs:
        assert p + q == target and isprime[p] and isprime[q]
        assert encoder(p) == word_p and encoder(q) == word_q
        if encoder == encode:
            assert decode(word_p) == p and decode(word_q) == q
        words += [word_p, word_q]
    assert len(pairs) == 5
    assert len(set([p for row in pairs for p in row[:2]])) == 10
    assert sorted(''.join(words)) == list(ALPHABET)
    return words


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Exact-cover search for five equal prime pairs')
    parser.add_argument('--plain', action='store_true', help='Use original uncoupled base-26 names')
    parser.add_argument('--limit', type=int, default=None, help='Largest target sum to check')
    args = parser.parse_args()
    encoder = encode_plain if args.plain else encode
    limit = args.limit if args.limit else (18250 if args.plain else 5000)
    found = find_pangram(limit, encoder)
    if found is None:
        print(f'No solution for {"plain" if args.plain else "coupled"} encoding up to N={limit}.')
    else:
        target, pairs = found
        words = verify(found, encoder)
        print('Found five prime pairs with common sum', target)
        for p, q, wp, wq, _ in pairs:
            print(f'{wp:>4} + {wq:<4} = {target}    ({p} + {q})')
        print('Pangram:', ' '.join(words))
        print('Alphabet:', ''.join(sorted(''.join(words))))
