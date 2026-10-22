import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from solution import fizzbuzz

def test_basic():
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]

def test_fizzbuzz_15():
    assert fizzbuzz(15)[-1] == "FizzBuzz"

def test_empty():
    assert fizzbuzz(0) == []
