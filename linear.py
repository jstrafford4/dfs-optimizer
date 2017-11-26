import sys, optimize, utils, settings
from pulp import *

class LinearOptimizer(optimize.Optimizer):



    def run(self):
        self.organize_players()
        # self.teams = self.random_teams(self.players_by_pos, self.restrictions, self.salary_cap, key=self.optimize_key, iterations=self.iterations)
        # self.best = self.teams[0]

    def organize_players(self):
        names = {}
        costs = {}
        points = {}
        for pos in self.players_by_pos.keys():
            players = self.players_by_pos[pos]
            for p in players:
                names[p.id] = p.first_name + ' ' + p.last_name
                costs[p.id] = p.salary
                points[p.id] = p.fppg

        prob = LpProblem("NFL Optimize 1", LpMaximize)

        myLpVars = {}
        sumArray = []
        for pos in self.players_by_pos:
            positionPlayers = self.players_by_pos[pos]
            myLpVars[pos] = LpVariable.dicts(pos, [p.id for p in positionPlayers],0,1,LpInteger)
            sumArray += [points[p.id] * myLpVars[pos][p.id] for p in positionPlayers]


        prob += lpSum(sumArray), "Total points of roster"

        for pos in self.restrictions.keys():
            prob += lpSum([myLpVars[pos][p.id] for p in self.players_by_pos[pos]]) == self.restrictions[pos], pos + " Requirement"

        prob += lpSum([costs[p.id] * myLpVars[p.position][p.id] for p in self.players_filtered]) <= self.salary_cap, "Salary Requirement"

        prob.writeLP("Test2.lp")
        prob.solve()

        print "Status:", LpStatus[prob.status]

        for v in prob.variables():
            if(v.varValue > 0):
                print v.name
        
        print "Points: ", value(prob.objective)


        # qbVars = LpVariable.dicts("qbs", [player.first_name + player.last_name for player in self.players_by_pos["QB"]], 0, 1, LpInteger)
        # rbVars = LpVariable.dicts("rbs", [player.first_name + player.last_name for player in self.players_by_pos["RB"]], 0, 1, LpInteger)
        # wrVars = LpVariable.dicts("wrs", [player.first_name + player.last_name for player in self.players_by_pos["WR"]], 0, 1, LpInteger)
        # teVars = LpVariable.dicts("tes", [player.first_name + player.last_name for player in self.players_by_pos["TE"]], 0, 1, LpInteger)
        # kVars = LpVariable.dicts("ks", [player.first_name + player.last_name for player in self.players_by_pos["K"]], 0, 1, LpInteger)
        # dVars = LpVariable.dicts("ds", [player.first_name + player.last_name for player in self.players_by_pos["D"]], 0, 1, LpInteger)

# just set these up, seriously.  Use Id's.
        

        # sumArray = []
        # sumArray += [p.fppg * qbVars[p.first_name + p.last_name] for p in self.players_by_pos["QB"]
        # sumArray += [p.fppg * rbVars[p.first_name + p.last_name] for p in self.players_by_pos["RB"]
        # sumArray += [p.fppg * wrVars[p.first_name + p.last_name] for p in self.players_by_pos["WR"]
        # sumArray += [p.fppg * teVars[p.first_name + p.last_name] for p in self.players_by_pos["TE"]
        # sumArray += [p.fppg * kVars[p.first_name + p.last_name] for p in self.players_by_pos["K"]
        # sumArray += [p.fppg * dVars[p.first_name + p.last_name] for p in self.players_by_pos["D"]

