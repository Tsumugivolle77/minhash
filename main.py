def kshingles_factory(k: int, digistring: str) -> set:
    is_present = set()
    kshingles = []
    dstring_len = len(digistring)
    start_pos, end_pos = 0, dstring_len - k + 1

    for i in range(start_pos, end_pos):
        kshingle = int(digistring[i:i + k])
        if kshingle not in is_present:
            is_present.add(kshingle)
            kshingles.append(kshingle)

    return kshingles


# %% 4.
import numpy as np

def generate_hash_functions(K, p=2147483647):
    a = np.random.randint(1, 10**12 + 1, size=K)  # Random coefficients
    b = np.random.randint(0, 10**12 + 1, size=K)  # Random intercepts
    return [(lambda x, a=a[i], b=b[i]: (a * x + b) % p) for i in range(K)]


def compute_signature_matrix(sets, K, N):
    hash_functions = generate_hash_functions(K)
    signature_matrix = np.full((K, len(sets)), float('inf'))  # Initialize with inf

    for i, current_set in enumerate(sets):
        for row, h in enumerate(hash_functions):
            # Apply hash function to each element in the set and take the minimum
            signature_matrix[row, i] = min(h(x) for x in current_set)

    return signature_matrix


# 5. a) generate sparse dataset
def generate_sparse_dataset(m, q, delta, N):
    dataset = []
    # Generate the first column with q random positions
    C0 = set(np.random.choice(N, q, replace=False))
    dataset.append(C0)

    for i in range(1, m):
        # Copy previous column
        previous_column = dataset[-1]
        current_column = set(previous_column)

        # Replace delta fraction of elements
        replace_count = int(delta * q)
        replace_positions = set(np.random.choice(list(previous_column), replace_count, replace=False))
        new_positions = set()
        while len(new_positions) < replace_count:
            candidate = np.random.randint(0, N)
            if candidate not in previous_column:
                new_positions.add(candidate)

        # Update current column
        current_column.difference_update(replace_positions)
        current_column.update(new_positions)
        dataset.append(current_column)

    return dataset

# %% Parameters for dataset
m = 100
q = 20000
delta = 0.02
N = 10**8

# Generate dataset
dataset = generate_sparse_dataset(m, q, delta, N)

# Parameters for signature matrix
K = 100  # Number of hash functions, for 5. b)

# Compute signature matrix
signature_matrix = compute_signature_matrix(dataset, K, N)

# Output signature matrix to a file
output_signature = "./signature_matrix.txt"
np.savetxt(output_signature, signature_matrix, fmt='%d')


# %% 5. c) compute jaccard similarity
from itertools import combinations

def compute_jaccard_similarity(set_a, set_b):
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0

# Compute Jaccard similarity for all pairs of columns
jaccard_similarities = []
for col1, col2 in combinations(range(len(dataset)), 2):
    similarity = compute_jaccard_similarity(dataset[col1], dataset[col2])
    jaccard_similarities.append((col1, col2, similarity))

# Save Jaccard similarities to a file
output_jaccard = "./jaccard_similarities.txt"
with open(output_jaccard, "w") as text_file:
    for col1, col2, sim in jaccard_similarities:
        text_file.write(f"Col {col1} - Col {col2}: Jaccard Similarity = {sim:.4f}\n")

text_file.close()