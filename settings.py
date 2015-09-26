


def filter_nfl(p, gametime=None, relax=True):
    if p.fppg < 3 or p.injury_indicator + p.injury_details != '':
        return False
    if gametime is not None and gametime not in p.gametime:
        return False
    return True

def filter_nhl(p, gametime=None, relax=True):
    if p.fppg < 1.0 or p.injury_indicator + p.injury_details != '':
        return False
    if p.played < 2:
        return False
    if gametime is not None and gametime not in p.gametime:
        return False
    return True

def filter_mlb(p, gametime=None, relax=True):
    if p.fppg < 1 or p.injury_indicator + p.injury_details != '':
        return False
    if p.position == 'P' and not relax and (p.probable_pitcher != 'Yes' or p.played < 10):
        return False
    if p.position != 'P' and not relax and (p.played < 35 or p.batting_order in ['', 0]):
        return False
    if gametime is not None and gametime not in p.gametime:
        return False
    return True

config = {
        'FanDuel': {'MLB': {'salary': 35000,
                       'composition': {'P':1, 'C':1, '1B':1, '2B':1, '3B':1, 'SS':1, 'OF':3},
                       'filter': filter_mlb
                      },
               'NFL': {'salary': 60000,
                       'composition': {'QB': 1, 'RB': 2, 'WR': 3, 'TE':1, 'K':1, 'D':1},
                       'filter': filter_nfl
                      },
               'NHL': {'salary': 55000,
                       'composition': {'LW': 2, 'RW': 2, 'C': 2, 'D': 2, 'G': 1},
                       'filter': filter_nhl
                      },
               },
        'DraftKings': {'MLB': {'salary': 35000,
                       'composition': {'P':2, 'C':1, '1B':1, '2B':1, '3B':1, 'SS':1, 'OF':3},
                       'filter': filter_mlb
                      },
               'NFL': {'salary': 60000,
                       'composition': {'QB': 1, 'RB': 2, 'WR': 3, 'TE':1, 'K':1, 'D':1},
                       'filter': filter_nfl
                      },
               'NHL': {'salary': 55000,
                       'composition': {'LW': 2, 'RW': 2, 'C': 2, 'D': 2, 'G': 1},
                       'filter': filter_nhl
                      },
               }
         }
