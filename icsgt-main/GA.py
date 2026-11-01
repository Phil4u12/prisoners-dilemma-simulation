import random
random.seed(42)

from Tournament import Tournament, Strategy

gene_key = ["AA", "CC", "CD", "DC", "DD"]

def genes_to_strategy(genes, name="GA_candidate"):
    """
    Turn a list of 5 numbers into a strategy and each of them represents how it is to cooperate
    in one of the five possible situations.Tis lets the GA evolve different behaviors by changing these numbers
    """
    table = dict(zip(gene_key, genes))
    return Strategy(table, name)

def random_genes():
    return [random.random() for _ in gene_key]#create a brand-new random individual.

def evaluate_fitness(genes, baseline_strategies, plays_per_match=50):
    """
    Measure how good a gene vector is by letting it play matches only against the baseline strategies:
    /candidate plays against each baseline once
    /baselines do not play each other
    final score of the candidate is used as its fitness
    higher score = better strategy
    """

    candidate = genes_to_strategy(genes, name="GA_candidate")

    #make fresh copies of baselines to avoid old scores sticking around
    players = [candidate] + [Strategy(b.strategy_table, b.name) for b in baseline_strategies]
    t = Tournament(players, plays_per_match=plays_per_match)
    fitness = t.run_ga_evaluation()

    return fitness

def select_parents(population, fitnesses, num_parents):
    """
    We pair each gene vector with its fitness, sort them by performance
    and take the top ones as “parents” for the neext generation

    These 'parents' are the ones whose behaviors we want to keep and mix
    """
    paired = list(zip(population, fitnesses))
    paired.sort(key=lambda x: x[1], reverse=True)
    return [p[0] for p in paired[:num_parents]]

def crossover(parent1, parent2):
    """
    We pick a random split point in the gene list and exchange the tails
    This mimics genetic mixing between two strategies, creating new ones
    """
    n = len(parent1)
    if n <= 1:
        return parent1[:], parent2[:]

    point = random.randint(1, n - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2


def mutate(genes, mutation_rate=0.1, mutation_std=0.1):
    """
    Each genen has a small chance of changing slightly by adding random noise
    This helps the GA explore new behaviors and avoid getting stuck

    After mutation, values are clipped back into 0, 1
    """
    new_genes = []
    for g in genes:
        if random.random() < mutation_rate:
            g = g + random.gauss(0, mutation_std)
        g = max(0.0, min(1.0, g))
        new_genes.append(g)

    return new_genes


def run_genetic_algorithm(
    baseline_strategies,
    population_size=20,
    num_generations=40,
    plays_per_match=50,
    num_parents=10,
    mutation_rate=0.1,
    mutation_std=0.1,
):
    """
    run the full ga process:

    The process works like this:
    1. Start with a population of random strategies
    2. For many generations:
        test how well each one does
        pick the best ones
        keep the very best few unchanged
        make new strategies by mixing and mutating the parents
    3. At the end, test everything one last time and return the best strategy

    this algorithm gradually improves the population and discovers a stratgy that performs strongly against all baselines
    """

    population = [random_genes() for _ in range(population_size)]
    history = []


    for gen in range(num_generations):#main GA loop

        #measure fitness
        fitnesses = [evaluate_fitness(genes, baseline_strategies, plays_per_match)for genes in population]

        best_f = max(fitnesses)
        avg_f = sum(fitnesses) / len(fitnesses)
        history.append((best_f, avg_f))
        print(f"Generation {gen}: best = {best_f:.2f}, avg = {avg_f:.2f}")

        parents = select_parents(population, fitnesses, num_parents)
        next_population = []
        next_population.extend(parents[:2])#keep the top 2 strategies unchanged


        while len(next_population) < population_size:
            p1, p2 = random.sample(parents, 2)

            c1, c2 = crossover(p1, p2)
            c1 = mutate(c1, mutation_rate, mutation_std)
            c2 = mutate(c2, mutation_rate, mutation_std)

            next_population.append(c1)
            if len(next_population) < population_size:
                next_population.append(c2)

        population = next_population #produce children until full

    #pick the strongest
    final_fitnesses = [evaluate_fitness(genes, baseline_strategies, plays_per_match)for genes in population]

    best_index = max(range(len(population)), key=lambda i: final_fitnesses[i])
    best_genes = population[best_index]
    best_fitness = final_fitnesses[best_index]

    print("GA finished.")
    print("Best genes:", best_genes)
    print("Best fitness:", best_fitness)

    return best_genes, best_fitness, history


if __name__ == "__main__":
    #import the 13 baseline strategies
    from strategy import baseline_strategies

    best_genes, best_fitness, history = run_genetic_algorithm(
        baseline_strategies=baseline_strategies,
        population_size=30,
        num_generations=40,
        plays_per_match=200,
        num_parents=15,
        mutation_std=0.1,
    )

