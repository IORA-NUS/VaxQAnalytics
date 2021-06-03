
import dash_bootstrap_components as dbc
import dash, os

external_stylesheets = [dbc.themes.FLATLY, 'https://codepen.io/chriddyp/pen/bWLwgP.css', ]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# if os.environ["DASH_ENV"] == "production":
#     app.config.from_object("config.ProductionConfig")
# elif os.environ["DASH_ENV"] == "development":
#     app.config.from_object("config.DevelopmentConfig")
# elif os.environ["DASH_ENV"] == "testing":
#     app.config.from_object("config.TestingConfig")
# else:
#     app.config.from_object("config.LocalConfig")


