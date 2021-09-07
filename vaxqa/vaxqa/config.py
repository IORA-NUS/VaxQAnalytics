

ProductionConfig = {
    'DEBUG': False,
    'DATA_BACKEND': 's3',
    'SCENARIO': 'results_cleaned_20210527',
    'APPLICATION_ROOT': '/vaxqa'
}

DevelopmentConfig = {
    'DEBUG': True,
    'DATA_BACKEND': 'folder',
    'SCENARIO': 'results_cleaned_20210521',
    'PORT': 8100,
    'APPLICATION_ROOT': '/vaxqa'
}

LocalConfig = {
    'DEBUG': True,
    'DATA_BACKEND': 'folder',
    'SCENARIO': 'results_cleaned_20210527',
    'PORT': 8100,
    'APPLICATION_ROOT': '/vaxqa'
}

TestingConfig = {
    'DEBUG': True,
    'DATA_BACKEND': 'folder',
    'SCENARIO': 'results_cleaned_20210521',
    'PORT': 8100,
    'APPLICATION_ROOT': '/vaxqa'
}
