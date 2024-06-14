from eseas.core.github_actions import GithubActions
import pytest


def gth_testing():
    return GithubActions().is_testing()


reason_gth = "passing when github Actions "


skip_if_github = pytest.mark.skipif(gth_testing(), reason=reason_gth)
