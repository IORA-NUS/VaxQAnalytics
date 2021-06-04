import os

prod_settings = {
    'debug': False,
    'data_backend': 's3', # 'folder' | 's3'
    'scenario': 'results_cleaned_20210527', # 'results_cleaned_20210527' | 'results_cleaned_20210521'
    # port: DO NOT UPDATE
}

dev_settings = {
    'debug': False,
    'data_backend': 'folder', # 'folder' | 's3'
    'scenario': 'results_cleaned_20210527', # 'results_cleaned_20210527' | 'results_cleaned_20210521'
    'port': 8100
}

local_settings = {
    'debug': True,
    'data_backend': 'folder', # 'folder' | 's3'
    'scenario': 'results_cleaned_20210527', # 'results_cleaned_20210527' | 'results_cleaned_20210521'
    'port': 8100
}

if os.environ.get("DASH_ENV") == "prod":
    settings = prod_settings
elif os.environ.get("DASH_ENV") == "dev":
    settings = dev_settings
else:
    settings = local_settings
