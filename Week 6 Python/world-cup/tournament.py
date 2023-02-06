# Simulate a sports tournament

import csv
import sys
import random

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []
    # Read teams into memory from file
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        # Loop through rows in file and add to teams list
        for row in reader:
            # Convert rating to an integer
            row['rating'] = int(row['rating'])
            teams.append(row)
        print(teams)

    counts = {}
    # Simulate N tournaments and keep track of win counts
    for n in range(N):
        # Get winner of tournament
        winner = simulate_tournament(teams)
        # Add win to winner total
        if winner in counts:
            counts[winner] += 1
        # If first win add to dictionary
        else:
            counts[winner] = 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])
    print(winners)
    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""

    # Simulate rounds until one winner left
    while len(teams) != 1:
        teams = simulate_round(teams)
    return teams[0]['team']


if __name__ == "__main__":
    main()
