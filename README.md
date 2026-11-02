# prisoners-dilemma-simulation

# Evolution of Strategies in the Iterated Prisoner's Dilemma

Python simulation of a round-robin tournament between 12 strategies in the
iterated Prisoner's Dilemma, plus a genetic algorithm that evolves a new strategy.
Team project from from a Computational Science class at the University of Amsterdam

## Research questions
1. How does the number of repeated encounters affect strategy performance?
2. How do different payoff structures change the ranking?
3. How does the communication error rate (noise) affect cooperation?
4. Does including self-play change the ranking?
5. Can a genetic algorithm evolve a strategy that beats the baselines?

## Method
- 12 baseline strategies (TFT, GRIM, WSLS, ALLD, ...) defined by the probability
  of cooperating after each previous joint move.
- Every experiment is repeated 20 times and averaged to reduce randomness.
- Genetic algorithm: population 30, 40 generations, crossover and mutation.

## Key results
- Noise lowers all scores and weakens reciprocal strategies such as GEN and SOFTG.
- The GA improved the best fitness from about 5,080 to about 5,700.


## How to run
pip install matplotlib
python Tournament_Experiment.py   # runs all 4 experiments, saves plots in /plots
python GA_Plot.py                 # runs the genetic algorithm
python GUI.py                     # opens the GUI

## Files
- Tournament.py: tournament logic
- strategy.py: the 12 baseline strategies
- GA.py: genetic algorithm
- Tournament_Experiment.py: the four experiments
- GUI.py: Tkinter interface
