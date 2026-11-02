#pip install matplotlib
import os
import random
random.seed(42)

from strategy import baseline_strategies
from GA import run_genetic_algorithm

import matplotlib.pyplot as plt


def plot_GA(history):
#logging fitness evolution across generations
    gens = list(range(len(history)))#0123..
    top_scores = [h[0] for h in history]
    avg_scores = [h[1] for h in history]

    #plot
    plt.figure()

    plt.plot(gens, top_scores, label="Best fitness")
    plt.plot(gens, avg_scores, label="Average fitness")

    plt.xlabel("generation")
    plt.ylabel("fitness/total score vs baselines")
    plt.title("GA evolution of strategy performance")
    plt.legend()
    plt.savefig(os.path.join("plots","GA_evolution.png"),dpi=200)

    plt.show()


if __name__ == "__main__":
    best_genes, best_fitness, history = run_genetic_algorithm(
        baseline_strategies=baseline_strategies,
        population_size=30,
        num_generations=40,
        plays_per_match=200,
        num_parents=15,
        mutation_rate=0.1,
        mutation_std=0.1,
    )

    print("best fitness from GA:", best_fitness)

    plot_GA(history)
