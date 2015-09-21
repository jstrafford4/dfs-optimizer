


class Player(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        for k, v in kwargs.items(): 
            self.__setattr__(k, v)

    def __repr__(self):
        return 'Player(%2s: %2.2f $%d %s %s #%s)' % (self.position, self.fppg, self.salary, self.first_name, self.last_name, self.played)


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
        if players is not None:
            for p in players:
                self.update(p)

    def update(self, p):
        self.composition.__setitem__(p.position, self.composition.setdefault(p.position, 0) + 1)
        self.fppg += p.fppg
        self.played += p.played
        self.salary += p.salary
        self.players += [p]
        self.fppg_avg = self.fppg / float(len(self.players))
        self.salary_avg = self.salary / float(len(self.players))
        self.played_avg = self.played / float(len(self.players))
        
        
    def __repr__(self):
        return 'Team(%2.2f  $%d)' % (self.fppg, self.salary)
        
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
    
    
def load_data(fn, header=None):
    players = []
    with open(fn, 'r') as f:
        if header is None:
            header = f.readline().rstrip().split(',')
            header = map(lambda h:h.lower().replace(' ','_').replace('"', ''), header)
        for line in f:
            vals = line.rstrip().replace('"', '').split(',')
            vals = map(lambda v: try_num(v), vals)
            players += [Player(**dict(zip(header, vals)))]
    return players
             
        