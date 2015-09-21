import random

import utils
from utils import Team, Player


def generate_teams(players_by_pos, restrictions, salary_cap, drop=lambda t: False, n=500000, best=True, progress=True):
    teams = [Team([])]
    i = 1
    while i < n:
        if i % 100000 == 0 and progress:
            if best:
                print i, teams[0]
            else:
                print i
        team = []
        for pos, pos_players in players_by_pos.items():
            team += random.sample(pos_players, restrictions[pos])
        team = Team(team)
        if team.salary <= salary_cap and not drop(team):
            if best and team.fppg > teams[0].fppg:
                teams = [team]
                i += 1
            elif not best:
                teams += [team]
                i += 1
            else:
                i += 1
        elif best:
            i += 1
    return sorted(teams, key=lambda t: t.fppg, reverse=True)




restrictions_mlb = {'P': 1, 'C': 1, '1B': 1, '2B': 1, '3B': 1, 'SS': 1, 'OF': 3}

def filter_mlb(players):
    results = []
    for p in players:
        if p.fppg < 1 or p.injury_indicator + p.injury_details != '':
            continue
        if p.position == 'P' and (p.probable_pitcher != 'Yes' or p.played < 10):
            continue
        if p.position != 'P' and (p.played < 35 or p.batting_order in ['', 0]):
            continue
        results += [p]
    return results


    
    
if __name__ == '__main__':
    players = utils.load_data('data/FanDuel-MLB-2015-09-24-13099-players-list.csv')
    print 'Unfiltered:', len(players)
    players = filter_mlb(players)
    print 'Filtered  :', len(players)
    players_by_pos = utils.groupby('position', players)
    teams = generate_teams(players_by_pos, restrictions_mlb, 35000, n=1500000)
    print teams[0]
    print teams[0].played_avg
    for p in teams[0].players:
        print p
    