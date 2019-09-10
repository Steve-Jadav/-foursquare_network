# Instantiating a client
# Userless Access
from collections import defaultdict
from typing import Dict, List, Any, Union, Tuple

import foursquare

from settings import CLIENT_ID, CLIENT_SECRET, MAX_NODES

client = foursquare.Foursquare(CLIENT_ID, CLIENT_SECRET)


def getname(user):
    return user.get('firstname') + ' ' + user.get('lastname') if user.get('lastname') else user.get('firstname')


def crawl(userid, max_nodes=MAX_NODES):
    """ Takes the user id of some user. This id is used as a start id for the crawler.
        It takes all the friends of the passed user_id and then continues by adding friends of
        friends of friends. """

    network_data = []  # You will need to append dictionaries to this empty list for each user.
    nodes: list = []  # List of nodes that should go in the graph [id1, id2, id3...]
    edges: list = []  # List of tuples [(id1, id2), (id1, id3)...]

    stack = [userid]
    while stack and len(nodes) < MAX_NODES:
        userid = stack.pop()

        user = client.users(USER_ID=userid)['user']

        current_user = dict(userid=user.get('id'), name=getname(user), friendcount=user.get('friends').get('count'),
                            friends=[])

        nodes.append((current_user['userid'], {'name': current_user['name']}))

        user_friends = client.users.friends(USER_ID=userid)['friends']['items']

        for x in user_friends:
            stack.append(x.get('id'))
            edges.append((current_user['userid'], x.get('id')))
            current_user['friends'].append({'userid': x.get('id'), 'name': getname(x)})
            nodes.append((x.get('id'), {'name': getname(x)}))

            if len(nodes) > max_nodes:
                break

        network_data.append(current_user)

    print('Total number of nodes: ', len(nodes))
    print('Total number of edges: ', len(edges))

    return network_data, nodes, edges


if __name__ == '__main__':
    network_data, node_list, edge_list = crawl(123455)
