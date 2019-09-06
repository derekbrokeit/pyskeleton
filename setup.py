"""
Copyright 2019, Derek A. Thomas, All rights reserved.
"""
from setuptools import setup


def get_git_version():
    """
    Returns a repository version assuming the 3 possible structures:

    1. Git tag is present, returns "{tag}.{# of commits}+{sha}" with
       potential 'dirty' tag.  This is ideal for cases where tags are of the
       format: 'X.X'. Example output is '0.1.0+g59984c7'.
    2. Git repository without tags produces the format:
       "0.0.0+{sha}_{branch name}" Example output is '0.0.0+59984c7_master'.
    3. No git repository results in a version "0.0.0_UNKOWN" by default.
    """
    from subprocess import check_output, STDOUT, CalledProcessError

    # check for tag, assuming X.X versioning by tags
    command = "git describe --tags --long --dirty"
    try:
        git_version = (
            check_output(command.split(), stderr=STDOUT).strip().decode("utf-8")
        )
    except CalledProcessError:
        pass
    else:
        tag, commits, sha = git_version.split("-", 2)
        return f"{tag}.{commits}+{sha}"

    # assume this is still a git repo without tags
    sha_command = "git rev-parse --short HEAD"
    branch_command = "git rev-parse --abbrev-ref HEAD"
    try:
        sha = check_output(sha_command.split(), stderr=STDOUT).strip().decode("utf-8")
    except CalledProcessError:
        pass
    else:
        branch = check_output(branch_command.split()).strip().decode("utf-8")
        return f"0.0.0+{sha}_{branch}"

    # no git repository was found
    return "0.0.0_UNKNOWN"


setup(version=get_git_version())
