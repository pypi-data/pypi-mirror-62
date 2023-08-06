"""
Functions for working with filesystem paths.

The :func:`expandpath` function expands the tilde to $HOME and environment
variables to their values.

See Also
--------
:py:mod:`boltons:boltons.pathutils`

"""
import boltons.pathutils

__all__ = [
    "expandpath",
]


def expandpath(path):
    """
    Recursive shell-like expansion of environment variables and tilde home directory.

    Parameters
    ----------
    path: str, [str], None
        a single path, a list of paths, or none.

    Returns
    -------
    str, [str], None:
        a single expanded path, a list of expanded path, or none

    Example
    -------

    .. code-block:: python

        import os
        from torxtools import pathutils
        os.environ['SPAM'] = 'eggs'
        assert pathutils.expandpath(['~/$SPAM/one', '~/$SPAM/two']) == [os.path.expanduser('~/eggs/one'), os.path.expanduser('~/eggs/two')]

    See Also
    --------
    :py:func:`boltons:boltons.pathutils.expandpath`

    """

    def _expandpath(path):
        if path is None:
            return None
        if isinstance(path, list):
            return [_expandpath(p) for p in path]
        return boltons.pathutils.expandpath(path)

    return _expandpath(path)
