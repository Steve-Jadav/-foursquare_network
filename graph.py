import networkx
import collections

from typing import List
from matplotlib import pyplot
from plotly import express
from pandas import DataFrame

from data import collect, getname


def write_to_file(graph: networkx.graph, filename: str):
    node_link_data = networkx.readwrite.node_link_data(graph)
    with open(filename, 'w') as f:
        f.write(node_link_data)


def read_from_file(filename: str):
    pass


def create(nodes: List[dict], edges: List[tuple]):
    graph = networkx.Graph()
    graph.add_nodes_from((node['id'], node) for node in nodes)
    graph.add_edges_from(edges)
    return graph


def draw_network(graph: networkx.Graph):
    # pyplot.subplot(121)
    labels = {userid: getname(user) for userid, user in graph.nodes(data=True)}
    networkx.relabel_nodes(graph, labels)
    networkx.draw_random(graph, with_labels=True, font_weight='bold')
    pyplot.show()


def draw_degree_histogram(graph: networkx.Graph):
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    df = DataFrame(data={'degree': degree_sequence})
    fig = express.histogram(df, x="degree")
    fig.show()


def calculate_diameter(graph):
    pass


if __name__ == '__main__':
    nodes, edges = collect(123455)
    graph = create(nodes, edges)
    write_to_file(graph, 'data.json')
    # draw_network(graph)
    # draw_degree_histogram(graph)
