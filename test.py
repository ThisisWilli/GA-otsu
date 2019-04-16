import numpy as np
import random

# def init_chrome(N):
#         population = []
#         for i in range(N):
#             population.append(np.random.randint(0, 2, 8).tolist())
#         return population
#
#
# def bin_to_oct(chrom):
#         result = 0
#         for i in range(len(chrom) - 1, -1, -1):
#             if list[i] == 1:
#                 result += pow(2, len(chrom) - 1 - i)
#             else:
#                 pass
#         return result


# chrome1, chrome2 = random.randint(0, 8 - 1), random.randint(0, 8 - 1)
# print(chrome1, chrome2)
# a = [1, 2, 3, 4, 1, 2, 3, 4]
# b = [5, 6, 7, 8, 5, 6, 7, 8]
# a[4:], b[4:] = b[4:], a[4:]
# probability = [0.14, 0.49, 0.06, 0.31]
# print(probability[0:3])
# accu_probability = [0]
# print(sum(probability[:1]))
# for i in range(0, len(probability), 1):
#     accu_probability.append(sum(probability[0:i+1]))
# print(accu_probability)
# print(np.random.random(8))
# def init_chrome(N):
#     pop = []
#     for i in range(0, N):
#         pop.append(np.random.randint(0, 2, 8).tolist())
#     return pop
# print(init_chrome(8))
# for i in range(100):
#     print(np.random.randint(0, 8))
nums = np.random.randint(0, 2, 5)
print(nums, sum(nums))