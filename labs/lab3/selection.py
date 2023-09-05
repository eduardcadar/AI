from random import random, randint


def tournament_selection(population: list, num, no_participants):
    if num % 2 == 1:
        print("num should be even")
        return
    new_population = []
    while len(new_population) < num:
        parent1 = select_tournament_winner(population, no_participants)
        population.remove(parent1)
        parent2 = select_tournament_winner(population, no_participants)

        new_population.append(parent1.crossover(parent2))
        new_population.append(parent2.crossover(parent1))
    return new_population


def select_tournament_winner(population, no_participants):
    participants = []
    for _ in range(no_participants):
        r = randint(0, len(population) - 1)
        participants.append(population[r])
    return max(participants, key=lambda c: c.fitness)


def roulette_selection(population, num):
    if num % 2 == 1:
        print("num should be even")
        return
    fitnesses = [c.fitness for c in population]
    total_fitness = sum(fitnesses)
    rel_fitness = [f/total_fitness for f in fitnesses]
    probs = [sum(rel_fitness[:i+1]) for i in range(len(rel_fitness))]

    new_population = []
    while len(new_population) < num:
        parent1, parent2 = None, None

        r = random()
        for (i, individual) in enumerate(population):
            if r <= probs[i]:
                parent1 = individual
                break

        r = random()
        for (i, individual) in enumerate(population):
            if r <= probs[i]:
                parent2 = individual
                break
        pos = randint(0, len(parent1.communities) - 1)
        new_population.append(parent1.crossover(parent2, pos))
        new_population.append(parent2.crossover(parent1, pos))
    return new_population


