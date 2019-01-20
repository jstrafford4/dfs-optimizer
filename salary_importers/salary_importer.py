import nfldb

def try_num(n):
    try:
        return float(n)
    except:
        return n

class SalaryImporter(object):
    
    dk_update_sql = '''
            UPDATE game_player gp SET draftkings_salary = %(salary)s
                               FROM game g
                               WHERE gp.gsis_id = g.gsis_id
                               AND g.week = %(week)s
                               AND g.season_year = %(year)s
                               AND g.season_type = 'Regular'::season_phase
                               AND gp.player_id = %(player_id)s;
        '''

    fd_update_sql = '''
            UPDATE game_player gp SET fanduel_salary = %(salary)s
                               FROM game g
                               WHERE gp.gsis_id = g.gsis_id
                               AND g.week = %(week)s
                               AND g.season_year = %(year)s
                               AND g.season_type = 'Regular'::season_phase
                               AND gp.player_id = %(player_id)s;
        '''

    def __init__(self, file_name='', db=None):
        self.file_name = file_name
        if db is None:
            self.db = nfldb.connect()
        else:
            self.db = db

    def load_dk_data(self, week, year, db=None, file_name=None):
        pass

    def update_dk_salary(self, cursor, player_id, salary, week, year):
        cursor.execute(self.dk_update_sql, {'player_id': player_id, 'salary': salary, 'week': week, 'year': year})
    
    def update_fd_salary(self, cursor, player_id, salary, week, year):
        cursor.execute(self.fd_update_sql, {'player_id': player_id, 'salary': salary, 'week': week, 'year': year})


class RotoguruImporter(SalaryImporter):

    team_dict = {
        'tam': 'TB',
        'sfo': 'SF',
        'det': 'DET',
        'bal': 'BAL',
        'car': 'CAR',
        'cin': 'CIN',
        'lar': 'LA',
        'buf': 'BUF',
        'jac': 'JAC',
        'nor': 'NO',
        'nwe': 'NE',
        'lac': 'LAC',
        'gnb': 'GB',
        'mia': 'MIA',
        'sea': 'SEA',
        'kan': 'KC'
    }

    def get_team(self, team_str):
        if team_str.lower() in self.team_dict:
            return self.team_dict[team_str.lower()]
        else:
            return team_str.upper()

    def get_name(self, last_first_name):
        split_names = last_first_name.split(',')
        first_last = split_names[1].replace(' ', '') + ' ' + split_names[0]
        print(first_last)
        return first_last

    def load_dk_data(self, week, year, file_name=None, db=None):
        if file_name is None:
            file_name = '../data/draftkings/rotoguru/week' + str(week) + '.csv'
        
        if db is None:
            db = self.db
        
        cur = db.cursor()
        players = []
        with open(file_name, 'r') as f:
            header = f.readline().strip().split(';')
            header = map(lambda h:h.lower().replace(' ', '_').replace('"', ''), header)
            for line in f:
                vals = line.rstrip().replace('"', '').split(';')
                vals = map(lambda v: try_num(v), vals)
                kwargs = dict([(h, vals[i] if i < len(vals) else 0.0) for i,h in enumerate(header)])
                if (kwargs.get('name') is not None and kwargs.get('dk_salary') is not None):
                    players.append(kwargs)
                    print(kwargs)
        for player in players:
            if not isinstance(player['dk_salary'], float):
                print("no salary?", player)
                continue
            if player['pos'].lower() != 'def':
                continue
                player_match = nfldb.player_search(self.db, self.get_name(player['name']))
                if player_match[0] is not None:
                    print(player_match[0].player_id, player_match[0].first_name, player_match[0].last_name)
                    self.update_dk_salary(cur, player_match[0].player_id, player['dk_salary'], week, year)
                    print("updated", player['dk_salary'])
            else:
                # team defense
                team = self.get_team(player['team'])
                player_id = team
                if len(team) == 2:
                    player_id = '00-00000' + team
                elif len(team) == 3:
                    player_id = '00-0000' + team
                self.update_dk_salary(cur, player_id, player['dk_salary'], week, year)
                print(team, player_id, player['dk_salary'])
        db.commit()
        cur.close()

    def load_fd_data(self):
        pass
    


rgi = RotoguruImporter()
for week in range(6, 18):
    rgi.load_dk_data(week, 2017)