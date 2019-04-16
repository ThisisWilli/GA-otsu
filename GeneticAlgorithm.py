import numpy as np
import random
from otsu import my_otsu
from PIL import Image


class GeneticAlgorithm:
    def __init__(self, image, N, max_interation):
        self.image = np.array(image)
        self.N = N  # 种群个数
        self.population = self.init_chrome(self.N)
        self.max_interation = max_interation  # 迭代的最大次数

    # 将染色体转化为十进制数进行ostu比较
    def bin_to_oct(self, chrom):
        result = 0
        for i in range(len(chrom) - 1, -1, -1):
            if chrom[i] == 1:
                result += pow(2, len(chrom) - 1 - i)
            else:
                pass
        return result

    # 初始化N条染色体
    def init_chrome(self, N):
        population = []
        for i in range(0, N):
            population.append(np.random.randint(0, 2, 8).tolist())
        return population
        # population = []
        # for i in range(N):
        #     self.population.append(np.random.randint(0, 2, 8).tolist())
        # return self.population #返回类型为list

    # 获取每个种群的适应度
    def get_fitness(self):
        test_nums = []
        for pop in self.population:
            test_nums.append(self.bin_to_oct(pop))
        fitness = [my_otsu(self.image, i) for i in test_nums]
        #dicts = dict(zip(test_nums, fitness))
        return fitness

    # 对染色体进行选择,随机选择种群个数的染色体组，允许重复，实现轮盘选择法
    def select(self):
        new_population = []
        fitness = self.get_fitness()
        sum_fitness = np.sum(fitness)
        probability = fitness / sum_fitness
        # 计算累计概率
        accu_probability = [0]
        for i in range(0, len(probability), 1):
            accu_probability.append(sum(probability[0:i+1]))
        # 产生N个0-1的随机数
        random_num = np.random.random(self.N)
        for num in random_num:
            for i in range(0, len(accu_probability), 1):
                if accu_probability[i] <= num <= accu_probability[i + 1]:
                    new_population.append(self.population[i])
                else:
                    pass

        # 选择过后种群变少了，或者变多了，需要重新生成，或者舍弃
        if len(new_population) < self.N:
            for i in range(0, self.N - len(new_population)):
                new_population.append(np.random.randint(0, 2, 8).tolist())
            self.population = new_population[:]
        elif len(new_population) > self.N:
            self.population = new_population[:self.N]

        # 产生N个0-1以内的随机数
        # random_num = np.random.random(0, 1, self.N)
        # choose_num = [i for i in range(self.N)]
        # fitness = self.get_fitness()
        # sum_fitness = np.sum(fitness)
        #
        # probability = fitness / sum_fitness
        # choosen_num = np.random.choice(choose_num, self.N, True, probability)
        # new_population = []
        # for i in choosen_num:
        #     new_population.append(self.population[i])
        # self.population = new_population[:]

    # 随机选择两对染色体进行交叉,染色体的后半段进行交换
    def cross(self):
        num1, num2 = random.randint(0, self.N - 2), random.randint(0, self.N - 2)
        cross_bits_num = 4
        self.population[num1][cross_bits_num:], self.population[num2][cross_bits_num:] = \
            self.population[num2][cross_bits_num:], self.population[num1][cross_bits_num:]

    # 选择染色体进行变异
    def mutate(self):
        # 计算变异的染色体个数
        # 进行退火操作
        mutate_num = 0.04 * self.N * 8
        mutate_num = int(mutate_num)
        for i in range(mutate_num):
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            pre_fitness = my_otsu(self.image, self.bin_to_oct(self.population[x]))
            if self.population[x][y] == 1:
                self.population[x][y] = 0
                # self.population[x][y] = pre_fitness < my_otsu(self.image,
                #                                               self.bin_to_oct(self.population[x])) and 0 or 1
                # if pre_fitness > my_otsu(self.image, self.bin_to_oct(self.population[x])): # 变异前的适应度值大于变异后的值
                #     self.population[x][y] = 0
                # else:
                #     random_nums = np.random.randint(0, 2, 5)
                #     if sum(random_nums) >= 2:
                #         self.population[x][y] = 1
                #     else:
                #         self.population[x][y] = 0
            else:
                self.population[x][y] = 1
                # self.population[x][y] = pre_fitness < my_otsu(self.image,
                #                                               self.bin_to_oct(self.population[x])) and 1 or 0
                # if pre_fitness > my_otsu(self.image, self.bin_to_oct(self.population[x])): # 变异前的适应度值大于变异后的值
                #     self.population[x][y] = 1
                # else:
                #     random_nums = np.random.randint(0, 2, 5)
                #     if sum(random_nums) >= 2:
                #         self.population[x][y] = 0
                #     else:
                #         self.population[x][y] = 1

    def get_threshold(self):
        best_thresholds, best_fitnesss = [], []
        inter_count = 0
        fitness = self.get_fitness()
        best_fitness = np.max(fitness)
        print(best_fitness)
        # 对种群进行灾变，如果5代只能还没有出现比之前更加优秀的种群，则后面的每次迭代都杀死最优秀的种群
        fiteness_max, sustain_num, cata_count = 0, 0, 0
        best_threshold = self.bin_to_oct(self.population[np.argmax(fitness)])
        while True:
            self.select()
            self.cross()
            self.mutate()
            fitness = self.get_fitness()
            if best_fitness < np.max(fitness):
                best_fitness = np.max(fitness)
                best_threshold = self.bin_to_oct(self.population[np.argmax(fitness)])
                inter_count += 1
                sustain_num = 0
            else:
                sustain_num += 1
                inter_count += 1
                if sustain_num >= 5:  # 五代以内都没有出现更好的种群,发生灾变
                    fitness_max = max(fitness)
                    for i in range(0, len(self.population)):
                        if my_otsu(self.image, self.bin_to_oct(self.population[i])) == fiteness_max:
                            self.population[i] = self.init_chrome(1)
                            cata_count += 1
                            if cata_count == 5:
                                sustain_num, cata_count = 0, 0
                        else:
                            pass

            if inter_count > self.max_interation:
                break
            print("适应度函数最大值为： {}".format(best_threshold))
            best_thresholds.append(best_threshold)
            print("最佳适应度为： {}".format(best_fitness))
            best_fitnesss.append(best_fitness)
            print()
        return best_threshold, best_thresholds, best_fitnesss, inter_count



