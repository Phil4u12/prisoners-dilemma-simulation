from tkinter import *
from tkinter import messagebox
from GA import run_genetic_algorithm
from Tournament import Tournament, Strategy
from strategy import baseline_strategies
from GA_Plot import plot_GA
import random

random.seed(42)


#helpers

def get_payoff_from_gui():
    """read payoff table from Tournament GUI entries"""
    payoff = {
        "CC": (int(CC_p1_entry.get()), int(CC_p2_entry.get())),
        "CD": (int(CD_p1_entry.get()), int(CD_p2_entry.get())),
        "DC": (int(DC_p1_entry.get()), int(DC_p2_entry.get())),
        "DD": (int(DD_p1_entry.get()), int(DD_p2_entry.get())),
    }
    return payoff


def validate_ga_inputs():
    """basic sanity checks for GA page inputs"""
    try:
        pop = int(population_entry.get())
        gens = int(generation_entry.get())
        plays = int(plays_entry.get())
        parents = int(num_parents_entry.get())
        mrate = float(mutation_rate_entry.get())
        mstd = float(mutation_std_entry.get())
    except ValueError:
        messagebox.showerror("Input error", "Please enter valid GA parameters.")
        return None

    if pop < 2:
        messagebox.showerror("Input error", "Population size must be >= 2.")
        return None
    if gens < 1:
        messagebox.showerror("Input error", "Generations must be >= 1.")
        return None
    if plays < 1:
        messagebox.showerror("Input error", "Plays per match must be >= 1.")
        return None
    if parents < 2 or parents > pop:
        messagebox.showerror("Input error", "Number of parents must be between 2 and population size.")
        return None
    if not (0.0 <= mrate <= 1.0):
        messagebox.showerror("Input error", "Mutation rate must be between 0 and 1.")
        return None
    if mstd < 0:
        messagebox.showerror("Input error", "Mutation std must be >= 0.")
        return None

    return pop, gens, plays, parents, mrate, mstd


def validate_tournament_inputs():
    """basic checks for Tournament inputs"""
    try:
        payoff = get_payoff_from_gui()
        plays = int(tm_plays_entry.get())
        err = float(tm_error_entry.get())
    except ValueError:
        messagebox.showerror("Input error", "Please enter valid Tournament parameters.")
        return None

    if plays < 1:
        messagebox.showerror("Input error", "Plays per match must be >= 1.")
        return None
    if not (0.0 <= err <= 1.0):
        messagebox.showerror("Input error", "Error rate must be between 0 and 1.")
        return None

    return payoff, plays, err


#GA

def run_ga():
    """run GA using parameters from GA page"""
    vals = validate_ga_inputs()
    if vals is None:
        return
    pop, gens, plays, parents, mrate, mstd = vals

    best_genes, best_fitness, history = run_genetic_algorithm(
        baseline_strategies=baseline_strategies,
        population_size=pop,
        num_generations=gens,
        plays_per_match=plays,
        num_parents=parents,
        mutation_rate=mrate,
        mutation_std=mstd
    )

    #show result in GUI
    messagebox.showinfo(
        "GA result",
        f"Best fitness: {best_fitness:.2f}\nBest genes: {best_genes}"
    )

    plot_GA(history)


def reset_ga():
    for entry, default in ga_params_for_reset:
        entry.delete(0, END)
        entry.insert(0, default)


def make_ga_parameter(name, default):
    row = Frame(parameter_frame, bg=bg_color)
    row.pack(anchor="w", pady=2)

    Label(row, text=name, width=16, bd=2, bg=bg_color, fg="white").pack(side=LEFT, padx=3, pady=2)
    entry = Entry(row, width=10)
    entry.pack(side=RIGHT, padx=1, pady=1)

    ga_params_for_reset.append((entry, default))
    return entry


#tournament

def run_tournament():
    """run baseline tournament using GUI parameters; show ranking in GUI"""
    vals = validate_tournament_inputs()
    if vals is None:
        return
    payoff, plays, err = vals

    mode = "self_matches" if selfplay_var.get() == 1 else "no_self_matches"

    baseline_tournament = Tournament(
        baseline_strategies,
        plays_per_match=plays,
        communication_error_rate=err,
        payoff=payoff,
        mode=mode,
    )
    baseline_tournament.run()

    # Display results in GUI text box
    results_text.delete("1.0", END)
    results_text.insert(END, f"Mode: {mode}\nPlays per match: {plays}\nError rate: {err}\n\n")
    for i, s in enumerate(baseline_tournament.strategies, start=1):
        results_text.insert(END, f"{i}. {s.name}: {s.score}\n")


def reset_tournament():#payoff defaults

    CC_p1_entry.delete(0, END); CC_p1_entry.insert(0, "3")
    CC_p2_entry.delete(0, END); CC_p2_entry.insert(0, "3")

    CD_p1_entry.delete(0, END); CD_p1_entry.insert(0, "0")
    CD_p2_entry.delete(0, END); CD_p2_entry.insert(0, "5")

    DC_p1_entry.delete(0, END); DC_p1_entry.insert(0, "5")
    DC_p2_entry.delete(0, END); DC_p2_entry.insert(0, "0")

    DD_p1_entry.delete(0, END); DD_p1_entry.insert(0, "1")
    DD_p2_entry.delete(0, END); DD_p2_entry.insert(0, "1")

    tm_plays_entry.delete(0, END); tm_plays_entry.insert(0, "200")
    tm_error_entry.delete(0, END); tm_error_entry.insert(0, "0.01")

    selfplay_var.set(0)
    results_text.delete("1.0", END)


#page navigation

def go_GA():
    GA_page.tkraise()

def go_Tournament():
    Tournament_page.tkraise()

def go_back():
    home_page.tkraise()


#app boot

GT_App = Tk()

bg_color = "#59298A"

GT_App.title("Run GA & Experiment GUI")
GT_App.geometry("520x420")
GT_App.config(bg=bg_color)

try:
    logo = PhotoImage(file="smiley.png")
    GT_App.iconphoto(True, logo)
except Exception:
    print("Logo not found or couldn't load")

home_page       = Frame(GT_App, bg=bg_color)
GA_page         = Frame(GT_App, bg=bg_color)
Tournament_page = Frame(GT_App, bg=bg_color)

for page in (home_page, GA_page, Tournament_page):
    page.grid(row=0, column=0, sticky="nsew")

#home page

home_page.tkraise()

go_GA_button = Button(home_page, text="Genetic Algorithm", command=go_GA)
go_GA_button.pack(pady=8)

go_Tournament_button = Button(home_page, text="Tournament", command=go_Tournament)
go_Tournament_button.pack(pady=8)


#GA page

parameter_frame = Frame(GA_page, bg=bg_color)
parameter_frame.pack(pady=8)

ga_params_for_reset= []

population_entry    = make_ga_parameter("Population size",    "20")
generation_entry    = make_ga_parameter("Generations",        "40")
plays_entry         = make_ga_parameter("Plays per match",    "50")
num_parents_entry   = make_ga_parameter("Number of parents",  "10")
mutation_rate_entry = make_ga_parameter("Mutation rate",      "0.1")
mutation_std_entry  = make_ga_parameter("Mutation std",       "0.1")

reset_ga()

ga_button_frame = Frame(GA_page, bg=bg_color)
ga_button_frame.pack(pady=6)

ga_reset_button = Button(ga_button_frame, text="Reset", command=reset_ga, relief=SUNKEN, bd=4, width=8)
ga_reset_button.grid(row=0, column=0, padx=5)

ga_run_button = Button(ga_button_frame, text="Run GA", command=run_ga, relief=SUNKEN, bd=4, width=12)
ga_run_button.grid(row=0, column=1, padx=5)

ga_back_button = Button(ga_button_frame, text="Go Back", command=go_back, relief=SUNKEN, bd=4, width=10)
ga_back_button.grid(row=1, column=0, columnspan=2, pady=6, sticky="ew")


#tournament page

payoff_frame = Frame(Tournament_page, bg=bg_color)
payoff_frame.pack(padx=5, pady=5)

Label(payoff_frame, text="", bg=bg_color, fg="white").grid(row=0, column=0)
Label(payoff_frame, text="P2: C", bg=bg_color, fg="white").grid(row=0, column=1, padx=5)
Label(payoff_frame, text="P2: D", bg=bg_color, fg="white").grid(row=0, column=2, padx=5)

Label(payoff_frame, text="P1: C", bg=bg_color, fg="white").grid(row=1, column=0, padx=5)
Label(payoff_frame, text="P1: D", bg=bg_color, fg="white").grid(row=2, column=0, padx=5)

#cells
def payoff_cell(r, c, d1, d2):
    cell = Frame(payoff_frame, bg=bg_color)
    cell.grid(row=r, column=c, padx=5, pady=3)
    e1 = Entry(cell, width=3); e1.insert(0, d1); e1.pack(side=LEFT, padx=1)
    e2 = Entry(cell, width=3); e2.insert(0, d2); e2.pack(side=LEFT, padx=1)
    return e1, e2

CC_p1_entry, CC_p2_entry = payoff_cell(1, 1, "3", "3")
CD_p1_entry, CD_p2_entry = payoff_cell(1, 2, "0", "5")
DC_p1_entry, DC_p2_entry = payoff_cell(2, 1, "5", "0")
DD_p1_entry, DD_p2_entry = payoff_cell(2, 2, "1", "1")

tm_params_frame = Frame(Tournament_page, bg=bg_color)
tm_params_frame.pack(padx=5, pady=(0, 8), anchor="w")

Label(tm_params_frame, text="Plays per match:", bg=bg_color, fg="white").grid(row=0, column=0, padx=5, pady=3, sticky="w")
tm_plays_entry = Entry(tm_params_frame, width=8)
tm_plays_entry.grid(row=0, column=1, padx=5, pady=3, sticky="w")
tm_plays_entry.insert(0, "200")

Label(tm_params_frame, text="Error rate:", bg=bg_color, fg="white").grid(row=1, column=0, padx=5, pady=3, sticky="w")
tm_error_entry = Entry(tm_params_frame, width=8)
tm_error_entry.grid(row=1, column=1, padx=5, pady=3, sticky="w")
tm_error_entry.insert(0, "0.01")

#selfplay toggle
selfplay_var = IntVar(value=0)
selfplay_check = Checkbutton(
    tm_params_frame, text="Include self-play",
    variable=selfplay_var, bg=bg_color, fg="white",
    activebackground=bg_color, selectcolor=bg_color
)
selfplay_check.grid(row=2, column=0, columnspan=2, padx=5, pady=3, sticky="w")

tm_button_frame = Frame(Tournament_page, bg=bg_color)
tm_button_frame.pack(pady=4)

tm_reset_button = Button(tm_button_frame, text="Reset", command=reset_tournament, relief=SUNKEN, bd=4, width=8)
tm_reset_button.grid(row=0, column=0, padx=5)

tm_run_button = Button(tm_button_frame, text="Run Tournament", command=run_tournament, relief=SUNKEN, bd=4, width=14)
tm_run_button.grid(row=0, column=1, padx=5)

tm_back_button = Button(tm_button_frame, text="Go Back", command=go_back, relief=SUNKEN, bd=4, width=10)
tm_back_button.grid(row=1, column=0, columnspan=2, pady=6, sticky="ew")

#results box
results_text = Text(Tournament_page, height=8, width=50)
results_text.pack(padx=8, pady=6)

reset_tournament()


GT_App.mainloop()
