import foursquare
import random

from settings import CLIENT_ID, CLIENT_SECRET, MAX_NODES, MAX_FRIENDS

client = foursquare.Foursquare(CLIENT_ID, CLIENT_SECRET)


def getname(user):
    return user.get('firstName') + ' ' + user.get('lastName') if user.get('lastName') else user.get('firstName')


def collect(userid, max_nodes=MAX_NODES):
    """
    Takes the userid of some user. This id is used as a start id for the crawler.
    It takes all the friends of the passed userid and then continues by adding random 
    friends of friends of friends.

    :param userid:
    :param max_nodes:
    :return: nodes and edges of the network graph
    """
    
    nodes: list = []  # List of nodes that should go in the graph [id1, id2, id3...]
    edges: list = []  # List of tuples [(id, id), (id, id)...]

    nodes.append(client.users(USER_ID=userid)['user'])
    stack = [userid]
    while stack and len(nodes) < max_nodes:
        userid = stack.pop()
        friends = client.users.friends(USER_ID=userid)['friends']['items']
        friends = random.sample(friends, MAX_FRIENDS) if len(friends) > MAX_FRIENDS else friends
        for friend in friends:
            stack.append(friend.get('id'))
            edges.append((userid, friend['id']))
            nodes.append(friend)

    print('Number of nodes: ', len(nodes), '\nNumber of edges: ', len(edges))
    return nodes, edges


if __name__ == '__main__':
    collect(123455)
