from mpmath import mp
import random

# sample code given by professor
def compute_k_shingles(s: str, k: int):
    """
    Compute k-shingles for a given string of digits.
    Return a sorted list of integers corresponding to the k-shingles.
    """
    shingles = set()
    for i in range(len(s) - k + 1):
        # Extract k-shingle
        k_shingle_str = s[i:i+k]
        # Convert to integer position
        k_shingle_int = int(k_shingle_str)
        shingles.add(k_shingle_int)
    return sorted(shingles)

example_s = "1234567"
example_k = 4
positions = compute_k_shingles(example_s, example_k)
print("Positions for s='1234567', k=4:", positions)

# Set precision (a bit higher than needed)
mp.dps = 10100
pi_str = str(mp.pi)
pi_digits = pi_str[2:10002]  # first 10,000 digits after decimal

k = 12
positions_pi = compute_k_shingles(pi_digits, k)

# Write to file
output_file = "pi_10000digits_k12_positions.txt"
with open(output_file, "w") as f:
    for pos in positions_pi:
        f.write(str(pos) + "\n")

print(f"Number of distinct k-shingles: {len(positions_pi)}")
print(f"Positions saved to {output_file}")

def minhash_signatures(positions, hash_funcs):
    """
    Compute the MinHash signature for a single column using given hash functions.

    Parameters:
    - positions: sorted list of integer positions of set bits.
    - hash_funcs: list of tuples (a, b, p)

    Returns:
    - A list containing the minhash signature, one entry per hash function.
    """
    signature = []
    N = 10**12
    for (a, b, p) in hash_funcs:
        min_val = None
        for x in positions:
            h = ((a*x + b) % p) % N+1
            if min_val is None or h < min_val:
                min_val = h
        signature.append(min_val)
    return signature

# Given parameters:
p_base = 10**15
hash_funcs = []
# First hash function:
hash_funcs.append((37, 126, p_base + 223))

# Generate remaining 4 hash functions
# p-values: p_base + 37, p_base + 91, p_base + 159, p_base + 187
p_offsets = [37, 91, 159, 187]
for i in range(4):
    a = random.randint(0, 10**12)
    b = random.randint(0, 10**12)
    p = p_base + p_offsets[i]
    hash_funcs.append((a, b, p))

print("Hash functions used (a,b,p):")
for hf in hash_funcs:
    print(hf)

# Run on pi_positions obtained above
signature = minhash_signatures(positions_pi, hash_funcs)

print("MinHash signature:", signature)

