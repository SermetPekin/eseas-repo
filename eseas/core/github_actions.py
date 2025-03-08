import sys


class GithubActions:
    def is_testing(self):
        return "hostedtoolcache" in sys.argv[0]


class PytestTesting:
    def is_testing(self):
        return "pytest" in sys.argv[0]


def get_input(msg, default=None):
    if GithubActions().is_testing() or PytestTesting().is_testing():
        if not default:
            print("currently testing with no default ")
            return False
        return default
    return input(msg)


