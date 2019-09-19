import networkx
import collections

from typing import List
from matplotlib import pyplot

from data import collect, getname


def create(nodes: List[dict], edges: List[tuple]):
    graph = networkx.Graph()
    graph.add_nodes_from((node['id'], node) for node in nodes)
    graph.add_edges_from(edges)
    return graph


def draw_network(graph: networkx.Graph):
    # pyplot.subplot(121)
    networkx.draw_random(graph, with_labels=True, font_weight='bold')
    labels = {userid: getname(user) for userid, user in graph.nodes(data=True)}
    networkx.relabel_nodes(graph, labels)
    pyplot.show()


def draw_degree_histogram(graph: networkx.Graph):
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = pyplot.subplots()
    pyplot.bar(deg, cnt, width=0.80, color='b')

    pyplot.title("Degree Histogram")
    pyplot.ylabel("Count")
    pyplot.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)

    # draw graph in inset
    pyplot.axes([0.4, 0.4, 0.5, 0.5])
    Gcc = sorted(networkx.connected_component_subgraphs(graph), key=len, reverse=True)[0]
    pos = networkx.spring_layout(graph)
    pyplot.axis('off')
    networkx.draw_networkx_nodes(graph, pos, node_size=20)
    networkx.draw_networkx_edges(graph, pos, alpha=0.4)

    pyplot.show()


def calculate_measures(graph):
    pass


if __name__ == '__main__':
    nodes, edges = collect(123455)
    graph = create(nodes, edges)
    draw_network(graph)
    draw_degree_histogram(graph)
