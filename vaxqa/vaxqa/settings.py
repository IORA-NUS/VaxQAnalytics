import os

prod_settings = {
    # 'env': 'local', # 'local' | 'dev' | 'prod
    'data_backend': 's3', # 'folder' | 's3'
    'scenario': 'results_cleaned_20210527', # 'results_cleaned_20210527' | 'results_cleaned_20210521'
    # port: DO NOT UPDATE
}

# dev_settings = {
#     # 'env': 'local', # 'local' | 'dev' | 'prod
#     'data_backend': 's3', # 'folder' | 's3'
#     'scenario': 'results_cleaned_20210527', # 'results_cleaned_20210527' | 'results_cleaned_20210521'
#     'port': 8100
# }

local_settings = {
    # 'env': 'local', # 'local' | 'dev' | 'prod
    'data_backend': 'folder', # 'folder' | 's3'
    'scenario': 'results_cleaned_20210527', # 'results_cleaned_20210527' | 'results_cleaned_20210521'
    'port': 8100
}

if os.environ.get("DASH_ENV") == "prod":
    settings = prod_settings
# elif os.environ.get("DASH_ENV") == "dev":
#     settings = dev_settings
else:
    settings = local_settings
