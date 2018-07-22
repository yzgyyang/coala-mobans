import sys
if sys.version_info < (3, ):
    try:
        import unittest2
        sys.modules['unittest'] = unittest2
    except ImportError:
        pass
