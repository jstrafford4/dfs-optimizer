import string


class Player(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.ownership = 0.0
        self.fppg_actual = 0.0
        self.gametime = ''
        self.game = '@'
        self.team = 'team'
        self.first_name = ''
        self.last_name = ''
        self.fppg = 0.0
        self.avgpointspergame = 0.0
        self.teamabbrev = 'team'
        self.injury_indicator = ''
        self.injury_details = ''
        self.probable_pitcher = ''
        self.played = 0
        self.batting_order = 0
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        if 'gameinfo' in kwargs:
            self.team = self.teamabbrev
            self.fppg = self.avgpointspergame
            g, t, tz = kwargs['gameinfo'].split(' ')
            self.game = g
            self.gametime = t + tz
            self.first_name = self.name.split(' ')[0]
            self.last_name  = ' '.join(self.name.split(' ')[1:])
        self.home_team = self.game.split('@')[1]
        self.away_team = self.game.split('@')[0]
        self.home = self.home_team == self.team
        self.odds = 0.0
        self.win_projected = 0

    def __repr__(self):
        return 'Player(%2s:%s %2.2f $%d %s %s Own:%2.2f t:%s Odds:%2.2f)' % (self.position, self.team, self.fppg, self.salary, self.first_name, self.last_name, self.ownership, self.gametime, self.odds)


class Team(object):
    def __init__(self, players=None):
        self.composition = {}
        self.players = []
        self.played = 0.0
        self.salary = 0.0
        self.fppg = 0.0
        self.fppg_avg = 0.0
        self.salary_avg = 0.0
        self.played_avg = 0.0
        self.ownership = 0.0
        self.teams = {}
        self.team_count = 0
        self.valid = True
        self.winners_projected = 0
        self.winners = 0
        self.players_dict = {}
        self.fppg_actual = 0.0
        self.odds = 0.0
        if players is not None:
            for p in players:
                self.update(p)

    def update(self, p):
        name = p.first_name + ' ' + p.last_name
        if name in self.players_dict:
            self.valid = False
        self.players_dict[name] = 1
        #self.hash += p.last_name
        self.composition.__setitem__(p.position, self.composition.setdefault(p.position, 0) + 1)
        if p.team not in self.teams:
            self.team_count += 1
        self.teams.__setitem__(p.team, self.teams.setdefault(p.team, 0) + 1)
        if self.teams[p.team] > 4:
            self.valid = False
        self.winners_projected += p.win_projected
        self.odds += p.odds
        self.fppg += p.fppg
        self.fppg_actual += p.fppg_actual
        self.ownership += p.ownership
        self.played += p.played
        self.salary += p.salary
        self.players += [p]
        self.fppg_avg = self.fppg / float(len(self.players))
        self.salary_avg = self.salary / float(len(self.players))
        self.played_avg = self.played / float(len(self.players))

    def __repr__(self):
        return 'Team(%2.2f  $%d Own:%2.2f WProj:%s Odds:%2.2f)' % (self.fppg, self.salary, self.ownership, self.winners_projected, self.odds)

class Entry(Team):
    def __init__(self, contest_id, entry_id, username, place, players=None):
        self.contest_id = contest_id
        self.entry_id = entry_id
        self.username = username
        self.place = place
        self.ownership_scaled = 1.0
        super(Entry, self).__init__(players)

    def update(self, p):
        self.winners += 1 if (p.home and p.home_score > p.away_score) else 1 if (not p.home and p.away_score > p.home_score) else 0
        super(Entry, self).update(p)

    def __repr__(self):
        return 'Entry(%s #%d Own:%2.2f $%d fppg:%2.2f) ' % (self.username, self.place, self.ownership, self.salary, self.fppg)


def try_num(n):
    try:
        return float(n)
    except:
        return n

def groupby(key, items):
    out = {}
    for i in items:
        k = i.__getattribute__(key)
        if k not in out:
            out[k] = []
        out[k] += [i]
    return out

def merge_ownership_data(fn, players, header=None):
    players_dict = dict([(p.first_name + ' ' + p.last_name, p) for p in players])
    players_dict[' shown on game day'] = Player(first_name='', last_name='shown on game day', position='na', fppg=0.0, salary=10000000, played=0.0)
    entries = {}
    with open(fn, 'r') as f:
        if header is None:
            header = f.readline().rstrip().split(',')
            header = map(lambda h:h.lower().replace(' ', '_').replace('"', ''), header)
        for line in f:
            vals = line.rstrip().replace('"', '').split(',')
            vals = map(lambda v: try_num(v), vals)
            contest_id = vals[0]
            entry_id = vals[1]
            username = vals[2]
            place = vals[3]
            name = vals[4] + ' ' + vals[5]
            position = vals[6]
            ownership = vals[7] if vals[7] != '' else 0.0
            gametime = vals[8]
            home_team = vals[9]
            home_score = vals[10]
            away_team = vals[11]
            away_score = vals[12]
            fppg_actual = vals[13] if vals[13] != '' else 0.0
            if entry_id not in entries:
                entries[entry_id] = Entry(contest_id, entry_id, username, place)
            if name in players_dict:
                players_dict[name].ownership = ownership
                players_dict[name].gametime = gametime
                players_dict[name].home_score = home_score
                players_dict[name].away_score = away_score
                players_dict[name].fppg_actual = fppg_actual
                entries[entry_id].update(players_dict[name])
    return sorted(entries.values(), key=lambda e:e.ownership, reverse=True)

def merge_ownership_data2(fn, players, header=None):
    players_dict = dict([(p.first_name + ' ' + p.last_name, p) for p in players])
    with open(fn, 'r') as f:
        if header is None:
            header = f.readline().rstrip().split(',')
            header = map(lambda h:h.lower().replace(' ', '_').replace('"', ''), header)
        for line in f:
            vals = line.rstrip().replace('"', '').split(',')
            vals = map(lambda v: try_num(v), vals)
            if vals[0] in players_dict:
                players_dict[vals[0]].ownership = vals[1]

def ownership_to_csv(fn, entries):
    header = 'contest_id,entry_id,place,username,salary,fppg,fppg_scaled,fppg_actual,ownership,ownership_scaled,team_count,winners,winners_projected,odds'
    hf = {'money': lambda e:1 if e.place <= 50 else 0}
    with open(fn, 'w') as f:
        f.write(header + ',' + ','.join(hf.keys()) + '\n')
        for e in entries:
            f.write(','.join(['%s' % e.__dict__[h] for h in header.split(',')]))
            f.write(',')
            f.write(','.join(['%s' % fn(e) for h, fn in hf.items()]))
            f.write('\n')

def load_data(fn, header=None):
    players = []
    with open(fn, 'r') as f:
        if header is None:
            header = f.readline().rstrip().split(',')
            header = map(lambda h:h.lower().replace(' ', '_').replace('"', ''), header)
        for line in f:
            vals = line.rstrip().replace('"', '').split(',')
            vals = map(lambda v: try_num(v), vals)
            kwargs = dict([(h, vals[i] if i < len(vals) else 0.0) for i,h in enumerate(header)])
            if '/' in kwargs['position']:
                pos1, pos2 = kwargs['position'].split('/')
                kwargs['position'] = pos1
                players += [Player(**kwargs)]
                kwargs['position'] = pos2
                players += [Player(**kwargs)]
            else:
                players += [Player(**kwargs)]
    return players


def calc_profit(winp=0.6,entries=20,fee=25,size=100,cut=0.1):
    return (winp * entries * (fee - (fee * cut * 2))) - ((1.0 - winp) * entries * fee)

mean = lambda x: sum(x) / float(len(x))
