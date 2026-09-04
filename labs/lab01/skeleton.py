import sys 
from dataclasses import dataclass

@dataclass
class TestCase:
    g: int
    p: int
    a: int
    b: int
    key: int

def parse_group(lines: list[str], group_number: int) -> TestCase:
    """Turn one group of 'label value' lines into a TestCase."""
    values = {}
    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(
                f"Test case {group_number}: expected 'label value', got {line!r}"
            )
        label, value = parts
        values[label] = int(value)

    expected = {"g", "p", "a", "b", "key"}
    missing = expected - values.keys()
    if missing:
        raise ValueError(
            f"Test case {group_number}: missing {', '.join(sorted(missing))}"
        )

    return TestCase(
        g=values["g"], p=values["p"], a=values["a"], b=values["b"], key=values["key"]
    )

def read_test_cases(path: str) -> list[TestCase]:
    """Read each text group in the file. Lines starting with # are comments."""
    with open(path) as f:
        text = f.read()

    test_cases = []
    current_group: list[str] = []
    for raw_line in text.splitlines() + [""]:  
        line = raw_line.strip()
        if line.startswith("#"):
            continue  
        if line:
            current_group.append(line)
        elif current_group:
            test_cases.append(parse_group(current_group, len(test_cases) + 1))
            current_group = []

    return test_cases

def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <data_filename.txt>")
        sys.exit(1)
    path = sys.argv[1]
    try:
        test_cases = read_test_cases(path)
    except FileNotFoundError:
        print(f"Error: file not found: {path}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Read {len(test_cases)} test case(s) from {path}\n")
    for i, tc in enumerate(test_cases, start=1):
        print(f"Test case {i}:")
        print(f"  g   = {tc.g}")
        print(f"  p   = {tc.p}")
        print(f"  a   = {tc.a}")
        print(f"  b   = {tc.b}")
        print(f"  key = {tc.key}")
        print()

main()