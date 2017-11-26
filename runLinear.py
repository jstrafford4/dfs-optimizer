import sys, optimize, utils, settings, linear

# if len(sys.argv) != 3:
#     print "Please specify a filename and FanDuel/DraftKings"
#     sys.exit()
# 
# playersFile = sys.argv[1]
# website = sys.argv[2]
# config = settings.config[website]['NFL']
# print config

o = linear.LinearOptimizer(settings.config['FanDuel']['NFL']['composition'],'data/fanduel/fdWeek12.csv',settings.config['FanDuel']['NFL']['salary'], player_filter=settings.config['FanDuel']['NFL']['filter'])
o.run()