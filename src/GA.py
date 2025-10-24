import random

# === Parameters ===
POP_SIZE = 1_000
GENERATIONS = 10
MUTATION_RATE = 0.1
TOTAL_TIME = 60
TRAFFIC = [26.0, 10.5, 23.5]  # traffic density for A, B, C


# === Create a random individual ===
def create_individual():
    times = sorted(random.sample(range(10, 50), 2))
    a = times[0]
    b = times[1] - times[0]
    c = TOTAL_TIME - times[1]
    return [a, b, c]


# === Fitness Function ===
def fitness(ind):
    waiting = sum(t / g for t, g in zip(TRAFFIC, ind))
    return 1 / waiting  # smaller waiting time = higher fitness


# === Crossover ===
def crossover(p1, p2):
    cut = random.randint(1, 2)
    child = p1[:cut] + p2[cut:]
    # Fix total = 60
    diff = TOTAL_TIME - sum(child)
    child[random.randint(0, 2)] += diff
    # Ensure all values are positive (at least 1)
    for i in range(len(child)):
        if child[i] < 1:
            child[i] = 1
    # Re-adjust to ensure total = 60
    total = sum(child)
    if total != TOTAL_TIME:
        diff = TOTAL_TIME - total
        child[random.randint(0, 2)] += diff
        # Final safety check
        for i in range(len(child)):
            if child[i] < 1:
                child[i] = 1
    return child


# === Mutation ===
def mutate(ind):
    if random.random() < MUTATION_RATE:
        idx = random.randint(0, 2)
        change = random.choice([-2, 2])
        ind[idx] = max(5, ind[idx] + change)  # keep positive
        diff = TOTAL_TIME - sum(ind)
        other_idx = random.randint(0, 2)
        ind[other_idx] += diff
        # Ensure all values remain positive (at least 1)
        for i in range(len(ind)):
            if ind[i] < 1:
                ind[i] = 1
        # Re-adjust if needed
        total = sum(ind)
        if total != TOTAL_TIME:
            diff = TOTAL_TIME - total
            ind[random.randint(0, 2)] += diff
    return ind


# === Main GA Loop ===
population = [create_individual() for _ in range(POP_SIZE)]

for gen in range(GENERATIONS):
    # Evaluate fitness
    fitness_scores = [(ind, fitness(ind)) for ind in population]
    fitness_scores.sort(key=lambda x: x[1], reverse=True)

    # Select top half
    top = [ind for ind, _ in fitness_scores[: POP_SIZE // 2]]

    # Create next generation
    new_pop = top.copy()
    while len(new_pop) < POP_SIZE:
        p1, p2 = random.sample(top, 2)
        new_pop.append(mutate(crossover(p1, p2)))

    population = new_pop
    best = fitness_scores[0]
    print(f"Gen {gen + 1}: Best = {best[0]}, Fitness = {best[1]:.4f}")

# === Final Result ===
best_solution = max(population, key=fitness)
print("\n🚦 Optimal Green Light Timings (sec):")
print(f"A: {best_solution[0]}s, B: {best_solution[1]}s, C: {best_solution[2]}s")
print(f"Fitness Score: {fitness(best_solution):.4f}")
