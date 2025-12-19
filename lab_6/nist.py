import math

from scipy.special import gammainc


def frequency_bit_test(sequence: str) -> float:
    """
    Frequency bit test
    :param sequence: bit sequence
    :return: p-value
    """
    n = len(sequence)
    x = 0
    for i in sequence:
        match i:
            case '1':
                x += 1
            case '0':
                x += -1

    s_n = abs(x) / math.sqrt(n)
    p_value = math.erfc(s_n / math.sqrt(2))
    return p_value


def identical_consecutive_bits_test(sequence: str) -> float:
    """
    Test for identical consecutive bits
    :param sequence: bit sequence
    :return: p-value
    """
    n = len(sequence)
    zeta = sequence.count('1') / n

    if abs(zeta - 0.5) >= (2 / math.sqrt(n)):
        return 0.0
    else:
        v_n = sum(1 for i in range(n - 1) if sequence[i] != sequence[i + 1])
        p_value = math.erfc(abs(v_n - 2 * n * zeta * (1 - zeta)) / (2 * math.sqrt(2 * n) * zeta * (1 - zeta)))
        return p_value


def longest_sequence_of_ones_test(sequence: str, pi: list, m: int) -> float:
    """
    Test for the longest sequence of ones in a block
    :param sequence: bit sequence
    :param pi: list of probabilities
    :param m: block size
    :return: p-value
    """
    v = [0, 0, 0, 0]

    blocks = [sequence[i:i + m] for i in range(0, len(sequence), m)]

    for block in blocks:
        counter = 0
        ones_count = 0

        for i in block:
            if i == '1':
                counter += 1
                ones_count = max(ones_count, counter)
            else:
                counter = 0
        match ones_count:
            case 0 | 1:
                v[0] += 1
            case 2:
                v[1] += 1
            case 3:
                v[2] += 1
            case _:
                v[3] += 1

    chi_square = 0
    for i in range(0, 4):
        chi_square += (((v[i] - 16 * pi[i]) ** 2) / (16 * pi[i]))

    p_value = gammainc(3 / 2, chi_square / 2)
    return p_value
