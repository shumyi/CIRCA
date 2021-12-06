"""
Test suites for DFSRanker
"""
import networkx as nx

from srca.alg.base import Score
from srca.alg.dfs import DFSScorer
from srca.model.case import CaseData
from srca.model.graph import MemoryGraph
from srca.model.graph import Graph
from srca.model.graph import Node


def test_dfs_scorer(graph: Graph, case_data: CaseData):
    """
    DFSScorer shall filter in anomalous nodes with no anomalous parents
    """
    latency = Node("DB", "Latency")
    traffic = Node("DB", "Traffic")
    saturation = Node("DB", "Saturation")
    scores = {
        latency: Score(2),
        traffic: Score(1),
        saturation: Score(3),
    }
    params = dict(data=case_data, scores=scores, current=case_data.detect_time + 60)

    scorer = DFSScorer(anomaly_threshold=0)
    # With an empty graph
    empty_graph = nx.DiGraph()
    empty_graph.add_nodes_from([latency, traffic, saturation])
    scores = scorer.score(graph=MemoryGraph(empty_graph), **params)
    assert set(scores.keys()) == {latency}
    # Search all nodes
    scores = scorer.score(graph=graph, **params)
    assert set(scores.keys()) == {traffic}
    # Filter out nodes
    scorer = DFSScorer(anomaly_threshold=2)
    scores = scorer.score(graph=graph, **params)
    assert set(scores.keys()) == {saturation}
