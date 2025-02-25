def split_evenly(x: int) -> tuple[int, int]:
    a = (x // 2) + 1 if x % 2 != 0 else x // 2
    b = x - a  # Ensure a + b = x
    return a, b

# Test cases
print(split_evenly(5))   # Expected output: (3, 2)
print(split_evenly(7))   # Expected output: (4, 3)
print(split_evenly(12))  # Expected output: (6, 6)
print(split_evenly(11))  # Expected output: (6, 5)
