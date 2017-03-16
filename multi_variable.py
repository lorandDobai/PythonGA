from random import randint, uniform, random
from math import log, sin

N = 100
X_RANGE = [-2, 2]
Y_RANGE = [-3, 7]
P_CROSSOVER = 0.1
P_MUTATION = 0.005
CHROM_LEN = 16
UPPER_BOUND = 2 ** (CHROM_LEN // 2)


def gen_pop():
    ret_pop = list()
    for i in range(N):
        x = bin(randint(0, UPPER_BOUND))[2:]
        y = bin(randint(0, UPPER_BOUND))[2:]
        ret_pop.append(x.rjust(CHROM_LEN // 2, '0') + y.rjust(CHROM_LEN // 2, '0'))
    return ret_pop


def chrom_value(chrom):
    x, y = value_x(chrom[:CHROM_LEN // 2], X_RANGE), value_x(chrom[CHROM_LEN // 2:], Y_RANGE)
    return func(x, y)


def value_x(x, intvl):
    a, b = intvl
    x = int(x, 2)
    return a + x * (b - a) / (UPPER_BOUND - 1)


def func(x, y):
    return 10 + log(x + 3) * (2 + sin(x * y))


def selection(pop):
    p_list = list()
    q_list = list()
    new_pop = list()
    S = 0
    for chrom in pop:
        tmp = chrom_value(chrom)
        S += tmp
        p_list.append(tmp)

    p_list = [(p / S) for p in p_list]
    accum = 0

    for p in p_list:
        accum += p
        q_list.append(accum)

    randoms = [uniform(0, 1) for i in range(N)]
    for r in randoms:
        prev = 0
        for index, q in enumerate(q_list):
            if prev <= r <= q:
                new_pop.append(pop[index])
                break
            prev = q

    return new_pop


def crossover(pop):
    new_pop = [c for c in pop]
    for index in range(0, N, 2):
        prob = random()
        if prob <= P_CROSSOVER:
            p1, p2 = new_pop[index], new_pop[index + 1]
            child_one = p1[:CHROM_LEN // 2] + p2[CHROM_LEN // 2:]
            child_two = p2[:CHROM_LEN // 2] + p1[CHROM_LEN // 2:]
            new_pop[index], new_pop[index + 1] = child_one, child_two
    return new_pop


def evolve(pop):
    new_pop = [c for c in pop]
    for index in range(N):
        prob = random()
        if prob <= P_MUTATION:
            x = bin(randint(0, UPPER_BOUND))[2:]
            y = bin(randint(0, UPPER_BOUND))[2:]
            new_pop[index] = x.rjust(CHROM_LEN // 2, '0') + y.rjust(CHROM_LEN // 2, '0')
    return new_pop


def genetic_algo():
    with open("output.txt", 'w') as fout:
        population = gen_pop()
        for generation in range(N // 2):

            population = evolve(crossover(selection(population)))
            output = ['#numar generatie: ' + str(generation) + '\n']
            for c in population:
                output.append('cromozom ' + c + '\n')
                output.append('valoare ' + str(chrom_value(c)) + '\n')
            fout.write(''.join(output))

        max_chrom = max(population, key=chrom_value)
        print(max_chrom, chrom_value(max_chrom))


if __name__ == '__main__':
    genetic_algo()
