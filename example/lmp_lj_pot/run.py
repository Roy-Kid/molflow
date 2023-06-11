import nni

search_space = {
    'eps': {'_type': "uniform", '_value': [0.1, 1.0]},
    'sig': {'_type': "uniform", '_value': [0.1, 1.0]}
}

params = {
    'eps': 1.0,
    'sig': 1.0
}

# setup MD simulation task
experiment = nni.Experiment('local')
experiment.config.trial_command = 'python run.py'
experiment.config.trial_code_directory = '.'
experiment.config.search_space = search_space

experiment.config.tuner.name = 'TPE'
experiment.config.tuner.class_args['optimize_mode'] = 'minimize'
# config.assessor.name = 'Medianstop

experiment.config.max_trial_number = 10
experiment.config.trial_concurrency = 2

experiment.run(9523)
