

ProductionConfig = {
    'DEBUG': False,
    'DATA_BACKEND': 's3',
    'SCENARIO': 'results_cleaned_20210527'
}

DevelopmentConfig = {
    'DEBUG': True,
    'DATA_BACKEND': 'folder',
    'SCENARIO': 'results_cleaned_20210521',
    'PORT': 8100,
}

LocalConfig = {
    'DEBUG': True,
    'DATA_BACKEND': 'folder',
    'SCENARIO': 'results_cleaned_20210527',
    'PORT': 8100,
}

TestingConfig = {
    'DEBUG': True,
    'DATA_BACKEND': 'folder',
    'SCENARIO': 'results_cleaned_20210521',
    'PORT': 8100,
}
