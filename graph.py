# For graph analysis
import networkx

# For handling data
import collections
import ujson
from pandas import DataFrame
from typing import List

# For visualization
from matplotlib import pyplot
import plotly
from plotly import express
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, plot

# Custom python code
from data import collect, getname


def write_to_file(graph: networkx.graph, filename: str):
    node_link_data = networkx.readwrite.node_link_data(graph)
    with open(filename, 'w') as f:
        f.write(ujson.dumps(node_link_data))


def read_from_file(filename: str):
    with open(filename) as f:
        node_link_data = f.read()
        node_link_data = ujson.loads(node_link_data)
        graph = networkx.readwrite.node_link_graph(node_link_data)

    return graph


def create(nodes: List[dict], edges: List[tuple]):
    """ Creates a graph from nodes and edges.
    :return: networkx.Graph object  """

    graph = networkx.Graph()
    graph.add_nodes_from((node['id'], node) for node in nodes)
    graph.add_edges_from(edges)
    return graph


def draw_network(graph: networkx.Graph):
    """ Generates an interactive graph network visualization
    in the form of an html page. The page is automatically
    redirected.
    """
    pos = networkx.random_layout(graph)

    edge_x = []
    edge_y = []
    for edge in graph.edges():
        edge_x.extend(tuple(pos[edge[0]]) + (None,))
        edge_y.extend(tuple(pos[edge[1]]) + (None,))

    edge_trace = go.Scatter(x=edge_x, y=edge_y,
                            line=dict(width=0.5, color="black"),
                            hoverinfo='none',
                            mode='lines')

    node_x = []
    node_y = []
    # hovertext = []
    for userid, user in graph.nodes(data=True):
        x, y = pos[userid]
        node_x.append(x)
        node_y.append(y)
        # hovertext.append(getname(user))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        # hovertext=hovertext,
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='Viridis',
            reversescale=True,
            color=[],
            size=12,
            colorbar=dict(
                thickness=15,
                title='Degree of node',
                xanchor='left',
                titleside='right'
            )))

    node_adjacencies = []
    node_text = []
    for node, adjacency_dict in graph.adjacency():
        node_adjacencies.append(len(adjacency_dict))
        node_text.append('Name: ' + str(getname(graph.nodes[node])) +
                         '<br> Degree: ' + str(len(adjacency_dict)))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Foursquare Friendship Network',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="CSE 472 - Social Media Mining",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    plotly.offline.plot(fig, filename='Network.html')


def draw_page_rank(graph: networkx.Graph):
    """ Generates an interactive network visualization for
    pagerank distribution, in the form of an html page. 
    The page is automatically redirected. 
    """

    # Calculate pagerank
    page_rank = networkx.pagerank(graph)

    # Set layout of nodes on the plot
    pos = networkx.random_layout(graph)

    edge_x = []
    edge_y = []
    for edge in graph.edges():
        edge_x.extend(tuple(pos[edge[0]]) + (None,))
        edge_y.extend(tuple(pos[edge[1]]) + (None,))

    edge_trace = go.Scatter(x=edge_x, y=edge_y,
                            line=dict(width=0.5, color="black"),
                            hoverinfo='none',
                            mode='lines')

    node_x = []
    node_y = []
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='Hot',
            reversescale=True,
            color=[],
            size=[v * 6500 for v in page_rank.values()],
            colorbar=dict(
                thickness=15,
                title='Pagerank of node',
                xanchor='left',
                titleside='right'
            )))

    node_adjacencies = []
    node_text = []
    for node, adjacency_dict in graph.adjacency():
        node_adjacencies.append(len(adjacency_dict))
        node_text.append(' '.join(('Name:', str(getname(graph.nodes[node])), '<br>', 'Page Rank:', str(page_rank.get(node)))))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Foursquare Network Pagerank',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="CSE 472 - Social Media Mining",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    plotly.offline.plot(fig, filename='Pagerank.html')


def draw_degree_histogram(graph: networkx.Graph):
    """ Generates an interactive degree distribution plot
    for the network, in the form of an html page. 
    The page is automatically redirected. 
    """

    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    df = DataFrame(data={'degree': degree_sequence})
    fig = express.histogram(df, x="degree")
    plotly.offline.plot(fig, filename='Degree Distribution.html')


def draw_betweenness(graph: networkx.Graph):
    betweenness = networkx.betweenness_centrality(graph)
    pos = networkx.circular_layout(graph)

    edge_x = []
    edge_y = []
    for edge in graph.edges():
        edge_x.extend(tuple(pos[edge[0]]) + (None,))
        edge_y.extend(tuple(pos[edge[1]]) + (None,))

    edge_trace = go.Scatter(x=edge_x, y=edge_y,
                            line=dict(width=0.5, color="black"),
                            hoverinfo='none',
                            mode='lines')

    node_x = []
    node_y = []
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='Hot',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Pagerank of node',
                xanchor='left',
                titleside='right'
            )))

    node_adjacencies = []
    node_text = []
    for node, adjacency_dict in graph.adjacency():
        node_adjacencies.append(len(adjacency_dict))
        node_text.append(getname(graph.nodes[node]))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Foursquare Network Betweenness',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="CSE 472 - Social Media Mining",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    plotly.offline.plot(fig, filename='betweenness.html')


if __name__ == '__main__':
    # nodes, edges = collect(123455)
    # graph = create(nodes, edges)
    # write_to_file(graph, 'data.json')

    graph = read_from_file('data/data.json')
    draw_network(graph)
    # draw_page_rank(graph)
    # draw_degree_histogram(graph)
    # draw_betweenness(graph)
