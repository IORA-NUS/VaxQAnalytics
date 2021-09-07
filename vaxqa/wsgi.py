from vaxqa.vaxqa import server as application
from vaxqa.settings import settings

if __name__ == '__main__':
    application.run(debug = settings.get('debug') if settings.get('debug') is not None else True,
                    host='0.0.0.0',
                    port=8100)
    