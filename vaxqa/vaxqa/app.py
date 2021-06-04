from collections import namedtuple
import pkg_resources

# backup true function
_true_get_distribution = pkg_resources.get_distribution
# create small placeholder for the dash call
# _flask_compress_version = parse_version(get_distribution("flask-compress").version)
_Dist = namedtuple('_Dist', ['version'])


def _get_distribution(dist):
    if dist == 'flask-compress':
        return _Dist('1.9.0') # your flask-compress version
    else:
        return _true_get_distribution(dist)


# monkey patch the function so it can work once frozen and pkg_resources is of
# no help
pkg_resources.get_distribution = _get_distribution

from .vaxqa import app, server

