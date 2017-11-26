import sys, optimize, utils, settings

if len(sys.argv) != 3:
    print "Please specify a filename and FanDuel/DraftKings"
    sys.exit()

playersFile = sys.argv[1]
website = sys.argv[2]
config = settings.config[website]['NFL']
print config

o = optimize.RandomOptimizer(config['composition'], playersFile, config['salary'], player_filter=config['filter'])
o.run()
print o.best