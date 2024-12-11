# 4. a) generate k-shingles
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

# %% test kshingles_factory
# print(kshingles_factory(4, '1234567'))

# %% 4. b) generate kshingles
from mpmath import mp

mp.dps = 10000
first_1000_digits_of_pi = str(mp.pi).replace('.', '')
pi_shingles = kshingles_factory(12, first_1000_digits_of_pi)

# %% output to text
output_text = "./pi_shingles.txt"
with open(output_text, "w") as text_file:
    for shingle in pi_shingles:
        text_file.writelines(str(shingle) + "\n")

text_file.close()

# %% 4. c) compute signature
import numpy as np

# initialize hash functions
i_s = [37, 91, 159, 187]
a, b, p = [37], [126], [10**15 + 223] + [10**15 + i for i in i_s]
a += list(np.random.randint(low=0, high=10**12 + 1, size=4))
b += list(np.random.randint(low=0, high=10**12 + 1, size=4))

def hash_function_factory(a_s: list[int], b_s: list[int], p_s: list[int]):
    abps = list(zip(a_s, b_s, p_s))
    print(abps)
    return [lambda x, a=a, b=b, p=p: (a * x + b) % p for a, b, p in abps]

def compute_minhash_signature(shingles, hash_funcs):
    signature = []
    for h in hash_funcs:
        signature.append(min(h(shin) for shin in shingles))
    return signature

hashs = hash_function_factory(a, b, p)
signature = compute_minhash_signature(pi_shingles, hashs)
print(f"Signature is: {signature}")