from Tournament import Strategy

gene_keys = ["AA", "CC", "CD", "DC", "DD"]

#strategy tables:
ALLC   = dict(zip(gene_keys, [1.0, 1.0, 1.0, 1.0, 1.0]))
ALLD   = dict(zip(gene_keys, [0.0, 0.0, 0.0, 0.0, 0.0]))
RND    = dict(zip(gene_keys, [0.5, 0.5, 0.5, 0.5, 0.5]))
GRIM   = dict(zip(gene_keys, [1.0, 1.0, 0.0, 0.0, 0.0]))
GEN    = dict(zip(gene_keys, [1.0, 1.0, 0.0, 1.0, 0.1]))
SUSP   = dict(zip(gene_keys, [0.0, 1.0, 0.1, 0.9, 0.0]))
WSLS   = dict(zip(gene_keys, [1.0, 1.0, 0.0, 0.0, 1.0]))
SOFTG  = dict(zip(gene_keys, [1.0, 1.0, 0.2, 1.0, 0.3]))
NCOOP  = dict(zip(gene_keys, [1.0, 0.9, 0.4, 0.8, 0.2]))
OPP    = dict(zip(gene_keys, [0.0, 0.2, 0.0, 0.9, 0.0]))
TFT    = dict(zip(gene_keys, [1.0, 1.0, 0.0, 1.0, 0.0]))
MCHV   = dict(zip(gene_keys, [1.0, 0.8, 0.0, 0.0, 0.1]))

#convert to Strategy objects

baseline_strategies = [
    Strategy(ALLC,  "ALLC"),
    Strategy(ALLD,  "ALLD"),
    Strategy(RND,   "RND"),
    Strategy(GRIM,  "GRIM"),
    Strategy(GEN,   "GEN"),
    Strategy(SUSP,  "SUSP"),
    Strategy(WSLS,  "WSLS"),
    Strategy(SOFTG, "SOFTG"),
    Strategy(NCOOP, "NCOOP"),
    Strategy(OPP,   "OPP"),
    Strategy(TFT,   "TFT"),
    Strategy(MCHV,  "MCHV")
]


'''
ALLC — Always Cooperate：Always plays C, no matter what happened before. It cooperates on the first move and continues to do so after CC, CD, DC, and DD. A very friendly but easily exploitable strategy.

ALLD — Always Defect：Always plays D in every situation. It never cooperates and ignores all past interactions. Very aggressive, but predictable.

RND — Random Strategy：Chooses C with probability 0.5 every round, independent of history. It doesn’t react to the opponent at all—its behaviour is purely random.

GRIM — Grim Trigger：Starts by cooperating and continues to cooperate as long as the opponent never defects.But once the opponent defects even once, GRIM switches to permanent defection.A very unforgiving strategy.

GEN — Generous Tit-for-Tat：A more forgiving version of Tit-for-Tat. It usually mirrors the opponent’s previous move, but after a defection it sometimes chooses to forgive and play C instead of retaliating immediately.

SUSP — Suspicious Tit-for-Tat：Similar to Tit-for-Tat, but begins with D instead of C.After the first move, it copies whatever the opponent did in the previous round.It behaves like TFT, but with an initial mistrust.

WSLS — Win-Stay, Lose-Shift (Pavlov Strategy)：Repeats its previous action if the last outcome was “good”.If the last outcome was “bad,” it switches (C-D or D-C).It learns from whether cooperation “worked” rather than copying the opponent.

SOFTG — Soft Grudger：Normally cooperates, but if the opponent defects, it punishes for a limited number of rounds by defecting back.Unlike GRIM, it eventually returns to cooperation, so it holds a temporary grudge rather than a permanent one.

NCOOP — Nearly Cooperate：Mostly cooperative, but with a small built-in chance of defecting in certain histories.An imperfect cooperator who slips into defection occasionally—due to “temptation” or “noise.”

OPP — Opposite Strategy：Tends to respond with the opposite of what the opponent did:more likely to defect after cooperation, and more likely to cooperate after a defection.This creates unpredictable but reactive behaviour.

TFT — Tit-for-Tat：The classic strategy: starts with C, then simply mirrors the opponent’s previous move.It is:nice (never defects first);retaliatory (punishes D immediately);forgiving (returns to C after the opponent cooperates)

MCHV — Machiavellian Strategy：A calculated strategy that cooperates most of the time but defects when the payoff is especially tempting.It tries to maintain a cooperative image while exploiting high-value opportunities—balancing “niceness” with opportunism.
'''