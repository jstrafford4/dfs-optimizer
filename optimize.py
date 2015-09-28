import random
import collections

import utils


class Optimizer(object):
    def __init__(self, restrictions, player_fn, salary_cap, iterations=1500000, optimize_key='fppg', player_filter=None, ownership_fn=None, odds_fn=None):
        self.restrictions = restrictions
        self.player_fn = player_fn
        self.ownership_fn = ownership_fn
        self.odds_fn = odds_fn
        self.player_filter = player_filter
        self.salary_cap = salary_cap
        self.iterations = iterations
        self.player_filter = (lambda p: True) if player_filter is None else player_filter
        self.optimize_key = optimize_key
        self.players = []
        self.load_players()
        self.players_filtered = self.players
        self.entries = []
        self.odds = {}
        if odds_fn is not None:
            self.merge_odds_data()
        if ownership_fn is not None:
            self.merge_ownership_data()
        self.players_by_pos = {}
        self.add_players(self.players_filtered)
        self.best = utils.Team([])
        self.teams = []
        self.player_counts = []

    def add_players(self, players, player_filter=None):
        self.players = sorted(players, key=lambda p:p.__dict__[self.optimize_key], reverse=True)
        self.players_filtered = filter(self.player_filter if player_filter is None else player_filter, self.players)
        self.players_by_pos = utils.groupby('position', self.players_filtered)
        if not all(k in self.players_by_pos for k in self.restrictions.keys()):
            raise Exception('[ERROR] Player list (players=%d) not sufficient to meet restrictions. Missing = %s.' % (len(players), [k for k in self.restrictions if k not in self.players_by_pos]))

    def load_players(self):
        self.players = utils.load_data(self.player_fn)

    def merge_ownership_data(self):
        self.entries = utils.merge_ownership_data(self.ownership_fn, self.players)
        m = max(self.entries, key=lambda e: e.ownership)
        f = max(self.entries, key=lambda e: e.fppg)
        for e in self.entries:
            e.ownership_scaled = e.ownership / float(m.ownership)
            e.fppg_scaled = e.fppg / float(f.fppg)

    def merge_odds_data(self):
        with open(self.odds_fn, 'r') as f:
            for line in f:
                away, away_odds, home, home_odds = line.rstrip().split(',')
                self.odds['%s@%s' % (away, home)] = (float(away_odds), float(home_odds))
        for p in self.players:
            p.odds = self.odds[p.game][p.home]
            p.win_projected = self.odds[p.game][p.home] > self.odds[p.game][not p.home]


    def optimize(self, iterations=None, optimize_key=None):
        self.iterations = self.iterations if iterations is None else iterations
        self.optimize_key = self.optimize_key if optimize_key is None else optimize_key
        self.run()
        self.count_players()

    def ownership_coverage(self):
        coverage = {}
        for k, v in self.players_by_pos.items():
            coverage[k] = 0
            for p in v:
                coverage[k] += p.ownership
        return coverage, utils.mean(coverage.values())

    def count_players(self):
        counts = {}
        for t in self.teams:
            for p in t.players:
                key = str(p)
                counts[key] = (p, counts.setdefault(key, (p, 0))[1] + 1)
        self.player_counts = sorted([(v[0], v[1]) for k,v in counts.items()], key=lambda p:p[1], reverse=True)

    def sort_teams(self, key):
        self.teams.sort(key=lambda t: t.__dict__[key], reverse=True)
        self.best = self.teams[0]

    def run(self):
        pass


class RandomOptimizer(Optimizer):
    def run(self):
        self.teams = self.random_teams(self.players_by_pos, self.restrictions, self.salary_cap, key=self.optimize_key, iterations=self.iterations)
        self.best = self.teams[0]

    def random_teams(self, players_by_pos, restrictions, salary_cap, key='fppg', drop=lambda t: False, iterations=1000000, keep=400, progress=250000):
        teams = collections.deque(maxlen=keep)
        teams.append(utils.Team([]))
        teams.append(utils.Team([]))
        i = 1
        while i <= iterations:
            if i % progress == 0:
                print i, teams[-1]
            i += 1
            team = []
            for pos, n in restrictions.items():
                team += random.sample(players_by_pos[pos], n)
            team = utils.Team(team)
            if team.hash == teams[-1].hash and team.players_dict == teams[-1].players_dict:
                continue
            if team.salary <= salary_cap and team.valid and not drop(team):
                if team.__dict__[key] >= teams[len(teams) / 2].__dict__[key] and team.winners_projected > 5:
                    teams.append(team)
        return sorted(teams, key=lambda t: t.__dict__[key], reverse=True)


