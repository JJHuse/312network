#!/usr/bin/python3


from CS312Graph import *
import time
import numpy as np


class NetworkRoutingSolver:
    def __init__( self):
        self.dist = []
        self.prevs = []

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        edges_left = 3
        while edges_left > 0:
            edge = node.neighbors[2]
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length
            node = edge.dest
            edges_left -= 1
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        self.dist, self.prevs = self.dijkstra(srcIndex)
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        t2 = time.time()
        return (t2-t1)
    
    def dijkstra(self, srcIndex: int):
        """Iterative method to find the shortest path from srcIndex to all other nodes in the network"""
        dist = [None] * len(self.network.nodes)
        dist[srcIndex] = 0
        prevs = [None] * len(self.network.nodes)
        priority_queue = array_heap()
        priority_queue.make_queue(self.network.nodes)

        while not priority_queue.is_empty():
            node = priority_queue.delete_min()
            for edge in node.neighbors:
                alt = dist[node.node_id] + edge.length
                if dist[edge.dest.node_id] is None or alt < dist[edge.dest.node_id]:
                    dist[edge.dest.node_id] = alt
                    prevs[edge.dest.node_id] = node.node_id
                    priority_queue.decrease_key(edge, alt)
        return dist, prevs


class array_heap:
    def __init__(self):
        self.heap = []
        self.edge_tracker = {}

    def is_empty(self) -> bool:
        """Returns True if the heap is empty, False otherwise"""
        return len(self.heap) == 0

    def make_queue(self, nodes: list):
        """Add every edge to the queue, then bubble to make it a heap"""
        for node in nodes:
            for edge in node.neighbors:
                self.heap.append(edge)
                self.edge_tracker[edge.get_nice_key()] = len(self.heap) - 1
        for edge in self.heap[::-1]:
            self.bubble_up(edge)

    def insert(self, edge: CS312GraphEdge):
        self.heap.append(edge)
        self.edge_tracker[edge.get_nice_key()] = len(self.heap) - 1
        self.bubble_up(edge)
    
    def bubble_up(self, edge: CS312GraphEdge):
        """Bring the edge up the heap until it is larger than its parent"""
        parent = self.get_parent(edge)
        if parent is not None and edge.length < parent.length:
            self.swap_edges(edge, parent)
            self.bubble_up(edge)
    
    def swap_edges(self, first, second):
        """Swap the positions of two edges in the heap"""
        first_index = self.edge_tracker[first.get_nice_key()]
        second_index = self.edge_tracker[second.get_nice_key()]
        self.edge_tracker[first.get_nice_key()] = second_index
        self.edge_tracker[second.get_nice_key()] = first_index
        self.heap[first_index] = second
        self.heap[second_index] = first

        
        

    def get_child(self, node: CS312GraphNode):
        """Calculate the positions of this node's children"""
        pass

    def get_parent(self, node: CS312GraphNode):
        """Calculate the position of this node's parent"""
        pass

    def bubble_down(self, edge: CS312GraphEdge):
        """Bring the edge down the heap until it is smaller than its children"""
        pass

    def delete_min(self) -> CS312GraphEdge:
        """Remove the smallest edge, switch the end edge to the top, and bubble it down"""
        pass

    def decrease_key(self, edge: CS312GraphEdge):
        """Decrease the key of the edge and bubble it up"""
        pass


