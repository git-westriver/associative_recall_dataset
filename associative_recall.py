import os
from itertools import product
import random

ALPH = "abcdefghijklmnopqrstuvwxyz"
N, K, Q = 1, 5, 1 # conf.len_of_keys, conf.num_of_keys, conf.num_of_queries

def create_associative_recall_dataset(N, K, Q, savedirname):
    M = 100000 # num of trains to create
    T = 1000 # num of tests to create
    Ngrams = ["".join(word) for word in product(ALPH, repeat=N)]
    for phase, num_data in [("train", M), ("test", T)]:
        print(f"phase: {phase}")
        for i in range(num_data):
            if i % 100 == 0: 
                print(f"{i} / {num_data}, {100*i // num_data} %")
            alphabets = "".join(random.sample(Ngrams, k=K))
            seq_list = []
            for j in range(K):
                k = alphabets[N*j: N*(j+1)]
                seq_list.append(k)
                seq_list.append(str(random.randint(0, 9)))
            rand_idx_list = [random.randint(0, K-1) for _ in range(Q)]
            for rand_idx in rand_idx_list:
                query = seq_list[rand_idx*2]
                seq_list.append(query)
                answer = seq_list[rand_idx*2+1]
                seq_list.append(answer)
            seq_str = "".join(seq_list)
            if phase == "train" and i <= 10:
                print(f"({i})", seq_str[:20], "...", seq_str[-20:])
            with open(f"{savedirname}/{phase}/{i}.txt", "w") as f:
                f.write(seq_str)

if __name__ == "__main__":
    dataset_dirname = f'associative-recall_N={N}_K={K}_Q={Q}_ALPH={len(ALPH)}'
    if not os.path.exists(f"{dataset_dirname}/test"):
        os.makedirs(f"{dataset_dirname}/train")
        os.makedirs(f"{dataset_dirname}/test")
    create_associative_recall_dataset(N, K, Q, dataset_dirname)