import networkx
import collections

from typing import List
from matplotlib import pyplot

from pandas import DataFrame

import plotly
from plotly import express
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

from data import collect, getname

#init_notebook_mode(connected = True)

def write_to_file(graph: networkx.graph, filename: str):
    node_link_data = networkx.readwrite.node_link_data(graph)
    with open(filename, 'w') as f:
        f.write(node_link_data)


def read_from_file(filename: str):
    pass


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
    redirected. """

    pos = networkx.random_layout(graph)
    networkx.draw(graph, pos = pos, node_color = 'black', node_size = 110,
                  edge_color = 'green', node_shape = 'o')
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)


    edge_trace = go.Scatter(x = edge_x, y = edge_y,
                       line = dict(width=0.5, color="black"),
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
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
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
    for node, adjacencies in enumerate(graph.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('Degree: ' + str(len(adjacencies[1])) + 
                          ', User ID: ' + str(adjacencies[0]))
    
    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text


    fig = go.Figure(data = [edge_trace, node_trace], 
               layout = go.Layout(
               title='<br>Foursquare Friendship Network',
               showlegend = False,
               hovermode = 'closest',
               margin = dict(b=20, l=5, r=5, t=40),
               annotations=[ dict(
                    text="CSE 472 - Social Media Mining",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
               )
    

    plotly.offline.plot(fig)
    #labels = {userid: getname(user) for userid, user in graph.nodes(data=True)}


def draw_degree_histogram(graph: networkx.Graph):
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    df = DataFrame(data={'degree': degree_sequence})
    fig = express.histogram(df, x="degree")
    fig.show()


def draw_betweenness_centrality(graph: networkx.Graph):
    

def calculate_diameter(graph):
    pass


if __name__ == '__main__':
    nodes, edges = collect(123455)
    graph = create(nodes, edges)
    #write_to_file(graph, 'data.json')

    # Network visualisation
    #draw_network(graph)

    # Degree distribution histogram
    #draw_degree_histogram(graph)

    # Betweenness histogram
    draw_between_centrality(graph)