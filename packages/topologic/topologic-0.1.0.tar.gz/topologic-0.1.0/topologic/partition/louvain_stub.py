# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import community
import networkx as nx
from typing import Any, Dict, Optional


def louvain(
    graph: nx.Graph,
    partition: Optional[Dict[Any, int]] = None,
    weight_attribute: str = 'weight',
    resolution: float = 1.0,
    random_state: Any = None
) -> Dict[Any, int]:
    """
    Compute the partition of the graph nodes which maximises the modularity (or try..) using the Louvain heuristics

    This is the partition of highest modularity, i.e. the highest partition of the dendrogram generated by the Louvain
    algorithm.

    This louvain function is a limited wrapper to the
    `community.best_partition <https://python-louvain.readthedocs.io/en/latest/api.html#community.best_partition>`_
    function in the `python-louvain <https://github.com/taynaud/python-louvain>`_ library written
    by `Thomas Aynaud <https://github.com/taynaud>`_.

    :param networkx.Graph graph: the networkx graph which is decomposed
    :param partition: the algorithm will start using this partition of the nodes. It's a
        dictionary where keys are their nodes and values the communities
    :type partition: Optional[Dict[Any, int]]
    :param str weight_attribute: the key in graph to use as weight. Default to 'weight'
    :param float resolution: Will change the size of the communities, default to 1. represents the time described in
        "Laplacian Dynamics and Multiscale Modular Structure in Networks", R. Lambiotte, J.-C. Delvenne, M. Barahona
    :param Any random_state: If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.
    :return: The partition, with communities numbered from 0 to number of communities
    :rtype: Dict[Any, int]
    :raises: NetworkXError - If the graph is not Eulerian.

    References
    1. Blondel, V.D. et al. Fast unfolding of communities in large networks. J. Stat. Mech 10008, 1-12(2008).
    """
    return community.best_partition(
        graph=graph,
        partition=partition,
        weight=weight_attribute,
        resolution=resolution,
        random_state=random_state
    )
