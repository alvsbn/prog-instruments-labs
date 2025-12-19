import pytest
from nist import frequency_bit_test, identical_consecutive_bits_test, longest_sequence_of_ones_test


@pytest.mark.parametrize("sequence, description", [
    ("01" * 64, "чередование 01"),
    ("10" * 64, "чередование 10"),
    ("1" * 128, "все единицы"),
    ("0" * 128, "все нули"),
])
def test_frequency_bit_test_basic(sequence: str, description: str):
    result = frequency_bit_test(sequence)
    assert 0 <= result <= 1

    if "все единицы" in description or "все нули" in description:
        assert result < 0.1
    elif "чередование" in description:
        assert result > 0.01


def test_frequency_bit_test_single_bit():
    result1 = frequency_bit_test("1")
    result0 = frequency_bit_test("0")
    assert 0 <= result1 <= 1
    assert 0 <= result0 <= 1


def test_identical_consecutive_bits_test_all_ones():
    sequence = "1" * 128
    p_value = identical_consecutive_bits_test(sequence)
    assert p_value == 0.0


def test_identical_consecutive_bits_test_alternating():
    sequence = "01" * 64
    p_value = identical_consecutive_bits_test(sequence)
    assert p_value < 0.01


def test_longest_all_sequence_of_ones_zeros():
    sequence = "0" * 128
    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    p = longest_sequence_of_ones_test(sequence, pi, 8)
    assert 0.0 <= p <= 1.0


def test_longest_sequence_of_ones_all_ones():
    sequence = "1" * 128
    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    p = longest_sequence_of_ones_test(sequence, pi, 8)
    assert 0.0 <= p <= 1.0


def test_longest_sequence_of_ones_test_alternating():
    sequence = "01" * 64
    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    p = longest_sequence_of_ones_test(sequence, pi, 8)
    assert 0.0 <= p <= 1.0


def test_frequency_bit_test_with_mock_and_args(monkeypatch):
    captured_args = []
    def mock_erfc(x):
        captured_args.append(x)
        return 0.60

    monkeypatch.setattr("nist.math.erfc", mock_erfc)

    result1 = frequency_bit_test("01")
    result2 = frequency_bit_test("10")

    assert result1 == 0.60
    assert result2 == 0.60