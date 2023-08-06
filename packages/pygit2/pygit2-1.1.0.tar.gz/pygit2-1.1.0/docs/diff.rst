**********************************************************************
Diff
**********************************************************************

.. contents::

A diff shows the changes between trees, an index or the working dir.

.. automethod:: pygit2.Repository.diff

Examples

.. code-block:: python

    # Changes between commits
    >>> t0 = revparse_single('HEAD')
    >>> t1 = revparse_single('HEAD^')
    >>> repo.diff(t0, t1)
    >>> t0.diff(t1)           # equivalent
    >>> repo.diff('HEAD', 'HEAD^') # equivalent

    # Get all patches for a diff
    >>> diff = repo.diff('HEAD^', 'HEAD~3')
    >>> patches = [p for p in diff]

    # Get the stats for a diff
    >>> diff = repo.diff('HEAD^', 'HEAD~3')
    >>> diff.stats

    # Diffing the empty tree
    >>> tree = revparse_single('HEAD').tree
    >>> tree.diff_to_tree()

    # Diff empty tree to a tree
    >>> tree = revparse_single('HEAD').tree
    >>> tree.diff_to_tree(swap=True)

The Diff type
====================

.. autoclass:: pygit2.Diff
   :members: deltas, find_similar, merge, parse_diff, patch, patchid, stats

   .. method:: Diff.__iter__()

      Returns an iterator over the deltas/patches in this diff.

   .. method:: Diff.__len__()

      Returns the number of deltas/patches in this diff.


The Patch type
====================

Attributes:

.. autoclass:: pygit2.Patch
   :members: create_from, data, delta, hunks, line_stats, text

The DiffDelta type
====================

.. autoclass:: pygit2.DiffDelta
   :members:

The DiffFile type
====================

.. autoclass:: pygit2.DiffFile
   :members:

The DiffHunk type
====================

.. autoclass:: pygit2.DiffHunk
   :members:

The DiffStats type
====================

.. autoclass:: pygit2.DiffStats
   :members:

The DiffLine type
====================

.. autoclass:: pygit2.DiffLine
   :members:
