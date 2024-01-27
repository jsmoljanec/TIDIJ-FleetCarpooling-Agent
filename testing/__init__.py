import unittest

loader = unittest.TestLoader()
suite = loader.discover('', pattern='test_*.py')

runner = unittest.TextTestRunner()
runner.run(suite)
