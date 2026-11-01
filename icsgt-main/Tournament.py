import random
random.seed(42)

class Strategy:
    """
    This is a strategy for an iterated Prisoner's Dilemma.

    A strategy is has a `strategy_table` that maps the previous joint
    move of both players to the probability of cooperating in the next move.
    A strategy also contains a `score`, which keeps track of how well the 
    strategy is doing in a tournament
    """
     
    def __init__(self, strategy_table, name):
        """
        Initialize a new strategy.

        Parameters
        ----------
        strategy_table : dict[str, float]
            Mapping from a two-character string representing the previous
            joint move (e.g. "CC", "CD", "DC", "DD", "AA" for the first move)
            to the probability of cooperating (a float between 0.0 and 1.0).
        name : str
            Human-readable name of the strategy, used for printing results.
        score : int
            Score that this strategy gained (in a tournament)
        """
        self.name = name 
        self.strategy_table = strategy_table
        self.score = 0
        self.previous_play = None

    def reset(self):
        """
        Reset the strategy state before a new tournament run or match.

        Currently this only resets the accumulated score, but the method
        can be expended if needed.
        """
        self.score = 0

    def move(self, opponent_play):
        """
        Currently not in use!
        """
        return "C" if self.strategy_table[self.previous_play + opponent_play] >= random.random() else "D"



class Tournament:
    """
    Class for a round-robin tournament for iterated Prisoner's Dilemma strategies.

    Each pair of strategies plays a fixed number of rounds. There is two modes. 
    Either a strategy also plays against itself or not. In each round,
    both players may suffer from a communication error where their intended
    move gets flipped (C ↔ D). Payoffs are accumulated as scores for each
    strategy and can be compared after the tournament.
    """
    def __init__(self, strategies,
                 plays_per_match = 200, 
                 communication_error_rate = 0.01, 
                 mode="no_self_matches",
                 payoff={"DD": (1, 1), "CD": (0, 5), "DC": (5, 0), "CC": (3, 3)}):
        """
        Create a new Tournament instance.

        Parameters
        ----------
        strategies : list[Strategy]
            List of Strategy objects that will participate in the tournament.
        plays_per_match : int, optional
            Number of rounds each pair of strategies will play, by default 200.
        communication_error_rate : float, optional
            Probability (between 0.0 and 1.0) that a chosen move is flipped
            due to communication error, by default 0.01.
        mode : str, optional
            Determines whether strategies play against themselves.
            If set to "no_self_matches", only distinct pairs are matched.
            Any other value will also include self-matches (strategy vs itself).
        payoff : dict, optional
            Payoffs in the form of a dictionary
        """
        self.strategies = strategies
        self.plays_per_match = plays_per_match
        self.communication_error_rate = communication_error_rate
        self.mode = mode

        self.payoff = payoff


    def communication_error(self, play):
        """
        Apply a possible communication error to a single move.

        When a move is "C" then, With probability `communication_error_rate`, the move is flipped:
        "C" becomes "D". Otherwise it is returned unchanged.

        Parameters
        ----------
        play : str
            Intended move, "C" for cooperate or "D" for defect.

        Returns
        -------
        str
            The (possibly flipped) move after simulating communication noise.
        """
        if self.communication_error_rate >= random.random():
            # print("CE!!")
            if play == "C":
                return "D"
            elif play =="D":
                return "D"
        else:
            return play 
    
    def match(self, strategy_1, strategy_2):
        """
        Play a single iterated match between two strategies.

        The two strategies play `plays_per_match` rounds against each other.
        In each round, both strategies choose a move based on their
        `strategy_table` and the previous joint outcome. Their moves may be
        flipped by `coomunication_error`, and then payoffs from the payoff
        matrix are added to their scores.

        Parameters
        ----------
        strategy_1 : Strategy
            The first strategy in the match.
        strategy_2 : Strategy
            The second strategy in the match.
        """
        previous_play = "AA" # 'AA' marks the first play, as it is the same read from front as from back

        for play in range(self.plays_per_match):
            play_1 = "C" if strategy_1.strategy_table[previous_play] >= random.random() else "D"
            play_2 = "C" if strategy_2.strategy_table[previous_play[::-1]] >= random.random() else "D"

            play_1 = self.communication_error(play_1)
            play_2 = self.communication_error(play_2)

            # print(f"Move1: {play_1}")
            # print(f"Move2: {play_2}")
            previous_play = play_1 + play_2
            gain_1, gain_2 = self.payoff[previous_play]
            strategy_1.score += gain_1
            strategy_2.score += gain_2

        # print(f"{strategy_1.name} score: {strategy_1.score}")
        # print(f"{strategy_2.name} score: {strategy_2.score}")

    def run_ga_evaluation(self):
        """
        GA fitness evaluation：
        /not include baseline vs baseline matches
        /not include candidate vs itself
        /returns the final score of the candidate
        """
        for s in self.strategies:
            s.reset()
        candidate = self.strategies[0]

        for baseline in self.strategies[1:]: #play candidate vs each baseline
            self.match(candidate, baseline)

        return candidate.score
    
    def run(self):
        """
        Run the full tournament for all registered strategies.

        This will:
        1. Reset all strategies.
        2. Run a match for each pair of strategies:
           - If `mode` is "not_aggainst_self", only distinct pairs are used.
           - Otherwise, strategies also play against themselves.
        3. Sort the strategies in place by their final score in descending order.
        4. Print the final ranking and scores.
        """
        for strategy in self.strategies:
            strategy.reset() 

        
        if self.mode == "no_self_matches":
            for i, strategy_1 in enumerate(self.strategies):
                for strategy_2 in self.strategies[i+1:]:
                    # print(f"Match: {strategy_1.name} vs {strategy_2.name}")
                    self.match(strategy_1, strategy_2)
        else:
            for i, strategy_1 in enumerate(self.strategies):
                for strategy_2 in self.strategies[i:]:
                    # print(f"Match: {strategy_1.name} vs {strategy_2.name}")
                    self.match(strategy_1, strategy_2)

        
        
        self.strategies.sort(key=lambda s: s.score, reverse=True)
        
        print("End")
        for strategy in self.strategies:
            print(f"{strategy.name} score: {strategy.score}")  
        



            
