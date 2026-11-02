"""
This script automatically runs the four experiments in Tournament.py:
1. reencounters
2. payoff table
3. communication error rate
4. self-play vs no-self-play
ps:each experiment will run repeated tournaments;have averages results;produces clean plots saved in a file called plots
"""

import os
import random
from copy import deepcopy
import matplotlib.pyplot as plt

from Tournament import Tournament, Strategy
from strategy import baseline_strategies

random.seed(42)


#preparations before the experiments
def ensure_plots_dir(path="plots"):
    """create folder"""
    os.makedirs(path, exist_ok=True)
    return path

def fresh_players(strategies):
    """
    Tournament adds up scores inside Strategy objects so we must create fresh copies every time we run a new tournament
    /otherwise scores from earlier runs leak into later runs
    """
    return [Strategy(deepcopy(s.strategy_table), s.name) for s in strategies]


def run_tournament_once(
    strategies,
    plays_per_match=200,
    communication_error_rate=0.01,
    payoff=None,
    mode="no_self_matches",
    seed=None
):
    """ run one tournament under certain parameters and returns: {strategy_name: score}"""

    if seed is not None:
        random.seed(seed)

    if payoff is None:
        payoff = {"CC": (3,3), "CD": (0,5), "DC": (5,0), "DD": (1,1)}#default payoff=prisoners dilemma


    players = fresh_players(strategies)#fresh copies/so tournament state resets each time

    t = Tournament(
        players,
        plays_per_match=plays_per_match,
        communication_error_rate=communication_error_rate,
        payoff=payoff,
        mode=mode
    )
    t.run()

    return {s.name: s.score for s in t.strategies}#in dict form


def sweep_parameter(param_values, run_fn, repeats=20, base_seed=42):
    """
    *general helper for “sweep a parameter and average results”
    /param_values: list of values
    /run_fn: function takingto result dict
    /repeats: number of repeated tournaments to average out randomness
    returns:names;list of strategy names;mean_scores;std_scores
    """
    names = [s.name for s in baseline_strategies]
    mean_scores = {}
    std_scores = {}

    for v in param_values:
        bucket = {n: [] for n in names}#collect all repeated scores

        for r in range(repeats):
            seed = base_seed + r
            result = run_fn(v, seed=seed)
            for n in names:
                bucket[n].append(result[n])


        mean_scores[v] = {n: sum(bucket[n]) / repeats for n in names}#compute mean + std_dev
        std_scores[v] = {}
        for n in names:
            m = mean_scores[v][n]
            variance = sum((x - m)**2 for x in bucket[n]) / repeats
            std_scores[v][n] = variance**0.5

    return names, mean_scores, std_scores



#experiment 1 — Reencounters

def run_experiment_reencounters(
    plays_list=[5, 10, 20, 50, 100, 200, 500],
    error_rate=0.01,
    payoff=None,
    repeats=20
):
    """test how “number of repeated encounters” affects strategies"""
    plots_dir = ensure_plots_dir()

    def run_for_plays(pm, seed=None):#wrapper to inject plays_per_match into tournament
        return run_tournament_once(
            baseline_strategies,
            plays_per_match=pm,
            communication_error_rate=error_rate,
            payoff=payoff,
            mode="no_self_matches",
            seed=seed
        )

    names, mean_scores, _ = sweep_parameter(plays_list, run_for_plays, repeats=repeats)

    #plot
    plt.figure(figsize=(10, 5))
    for n in names:
        plt.plot(
            plays_list,
            [mean_scores[p][n] for p in plays_list],
            marker="o",
            label=n
        )

    plt.xlabel("Plays per match")
    plt.ylabel("Mean tournament score")
    plt.title("Experiment 1: Effect of repeated encounters")
    plt.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "reencounters.png"), dpi=200)
    plt.show()


#experiment 2 — Payoff table

def run_experiment_payoff(
    payoff_sets=None,
    plays_per_match=200,
    error_rate=0.01,
    repeats=20
):
    """how different payoff structures change strategy rankings"""
    plots_dir = ensure_plots_dir()


    if payoff_sets is None:#default payoff families to explore
        payoff_sets = {
            "Baseline PD": {"CC": (3,3), "CD": (0,5), "DC": (5,0), "DD": (1,1)},
            "High Temptation": {"CC": (3,3), "CD": (0,7), "DC": (7,0), "DD": (1,1)},
            "Coop-Friendly": {"CC": (4,4), "CD": (0,5), "DC": (5,0), "DD": (1,1)},
        }

    labels = list(payoff_sets.keys())

    def run_for_payoff(label, seed=None):
        return run_tournament_once(
            baseline_strategies,
            plays_per_match=plays_per_match,
            communication_error_rate=error_rate,
            payoff=payoff_sets[label],
            mode="no_self_matches",
            seed=seed
        )

    names, mean_scores, _ = sweep_parameter(labels, run_for_payoff, repeats=repeats)

    #decide to do grouped bar plot
    x = list(range(len(names)))
    width = 0.8 / len(labels)

    plt.figure(figsize=(12, 5))
    for i, lab in enumerate(labels):
        plt.bar(
            [xi + (i - len(labels)/2)*width + width/2 for xi in x],
            [mean_scores[lab][n] for n in names],
            width=width,
            label=lab
        )

    plt.xticks(x, names, rotation=45, ha="right")
    plt.ylabel("Mean tournament score")
    plt.title("Experiment 2: Effect of payoff table variations")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "payoff_tables.png"), dpi=200)
    plt.show()


#experiment 3 — Communication error rate

def run_experiment_noise(
    error_list=[0, 0.001, 0.01, 0.05, 0.1, 0.2],
    plays_per_match=200,
    payoff=None,
    repeats=20
):
    """
    test robustness under increasing communication noise
    no more with or without the communication error cause rate can be 0 which is 'without'
    """
    plots_dir = ensure_plots_dir()

    def run_for_error(er, seed=None):
        return run_tournament_once(
            baseline_strategies,
            plays_per_match=plays_per_match,
            communication_error_rate=er,
            payoff=payoff,
            mode="no_self_matches",
            seed=seed
        )

    names, mean_scores, _ = sweep_parameter(error_list, run_for_error, repeats=repeats)

    #plot
    plt.figure(figsize=(10, 5))
    for n in names:
        plt.plot(
            error_list,
            [mean_scores[e][n] for e in error_list],
            marker="o",
            label=n
        )

    plt.xlabel("Communication error rate")
    plt.ylabel("Mean tournament score")
    plt.title("Experiment 3: Effect of communication error")
    plt.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "noise_rate.png"), dpi=200)
    plt.show()


#experiment 4 — Self-play vs No-self-play

def run_experiment_selfplay(
    plays_per_match=200,
    error_rate=0.01,
    payoff=None,
    repeats=20
):
    """does including self-play change strategy rankings??"""
    plots_dir = ensure_plots_dir()

    names = [s.name for s in baseline_strategies]
    scores_no = {n: [] for n in names}
    scores_self = {n: [] for n in names}

    for r in range(repeats):
        seed = 42 + r

        #without self-play
        res_no = run_tournament_once(
            baseline_strategies,
            plays_per_match=plays_per_match,
            communication_error_rate=error_rate,
            payoff=payoff,
            mode="no_self_matches",
            seed=seed
        )

        #with self-play
        res_self = run_tournament_once(
            baseline_strategies,
            plays_per_match=plays_per_match,
            communication_error_rate=error_rate,
            payoff=payoff,
            mode="self_matches",  #any non-"no_self_matches" includes self-play
            seed=seed
        )

        for n in names:
            scores_no[n].append(res_no[n])
            scores_self[n].append(res_self[n])

    #average scores
    mean_no = {n: sum(scores_no[n]) / repeats for n in names}
    mean_self = {n: sum(scores_self[n]) / repeats for n in names}

    #decide to do paired bar plot
    x = list(range(len(names)))
    width = 0.38

    plt.figure(figsize=(12, 5))
    plt.bar([i - width/2 for i in x], [mean_no[n] for n in names],
            width=width, label="No self-play")
    plt.bar([i + width/2 for i in x], [mean_self[n] for n in names],
            width=width, label="With self-play")

    plt.xticks(x, names, rotation=45, ha="right")
    plt.ylabel("Mean tournament score")
    plt.title("Experiment 4: Self-play vs No-self-play")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "selfplay.png"), dpi=200)
    plt.show()


#run all experiments

if __name__ == "__main__":
    print("Running Experiment 1: Reencounters…")
    run_experiment_reencounters()

    print("Running Experiment 2: Payoff tables…")
    run_experiment_payoff()

    print("Running Experiment 3: Communication noise…")
    run_experiment_noise()

    print("Running Experiment 4: Self-play…")
    run_experiment_selfplay()

    print("All experiments finished. Plots saved in /plots/")
