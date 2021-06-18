import numpy as np
import os

path = '/home/lyn/ROUGE/ROUGE-1.5.5/RELEASE-1.5.5/'

test_src = []

with open(path + "/test_cnndm.src", "r") as f:
    for line in f:
        test_src.append(line)


def get_results():
    id = np.random.randint(0, 10000)
    while not os.path.exists(path + "sumGAN" + "/models/model." + str(id) +
                             ".txt"):
        id = np.random.randint(0, 10000)

    with open(path + "sumGAN" + "/models/model." + str(id) + ".txt") as f:
        s_model_a = f.readline()

    with open(path + "sumGAN" + "/systems/system." + str(id) + ".txt") as f:
        s_system = f.readline()

    with open(path + "abs-rl-rerank" + "/models/model." + str(id) +
              ".txt") as f:
        s_model_b = f.readline()

    # add a space after s_fairseq so the end is the same as s_other
    # end of s_fairseq "****** ."
    # end of s_other "****** . "
    return id, s_model_a + " ", s_model_b, s_system, test_src[id]
