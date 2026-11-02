import random
random.seed(42)

from Tournament import Tournament, Strategy
from strategy import baseline_strategies, gene_keys
from GA import run_genetic_algorithm

#first, run GA to get the evolved best genes
best_genes, best_fitness, history = run_genetic_algorithm(
    baseline_strategies=baseline_strategies,
    population_size=30,
    num_generations=40,
    plays_per_match=200,
    num_parents=15,
    mutation_rate=0.1,
    mutation_std=0.1,
)

print("Best genes from GA:", best_genes)
print("Best fitness from GA evaluation:", best_fitness)

#turn the best genes into a strategy object
evolved_table = dict(zip(gene_keys, best_genes))
Evolved = Strategy(evolved_table, "Evolved_GA")

#build a list of all players: 13 baselines + evolved strategy
all_players = baseline_strategies + [Evolved]

#run a full round-robin tournament using the original run method
t = Tournament(all_players, plays_per_match=200, mode="no_self_matches")
t.run()
