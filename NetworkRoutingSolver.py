#!/usr/bin/python3


from CS312Graph import *
import time
import numpy as np


class NetworkRoutingSolver:
    def __init__( self):
        self.distances = []
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
        while self.prevs[dest_index] is not None:
            prev_index = self.prevs[dest_index]
            precursor = self.network.nodes[prev_index]
            for edge in precursor.neighbors:
                if edge.dest.node_id == dest_index:
                    path_edges.insert(0, edge)
                    break
            dest_index = prev_index
        return {'cost':self.dest.distance, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        self.distances, self.prevs = self.dijkstra(srcIndex)
        t2 = time.time()
        return (t2-t1)
    
    def dijkstra(self, srcIndex: int):
        """Iterative method to find the shortest path from srcIndex to all other nodes in the network"""
        distances = [None] * len(self.network.nodes)
        distances[srcIndex] = 0
        prevs = [None] * len(self.network.nodes)
        priority_queue = array_heap()
        priority_queue.make_queue(self.network.nodes)

        while not priority_queue.is_empty():
            node = priority_queue.delete_min()
            for edge in node.neighbors:
                alt = distances[node.node_id] + edge.length
                if distances[edge.dest.node_id] is None or alt < distances[edge.dest.node_id]:
                    distances[edge.dest.node_id] = alt
                    prevs[edge.dest.node_id] = node.node_id
                    priority_queue.decrease_key(edge, alt)
        return distances, prevs


class array_heap:
    def __init__(self):
        self.heap = []
        self.heap_map = []

    def is_empty(self) -> bool:
        """Returns True if the heap is empty, False otherwise"""
        return len(self.heap) == 0

    def make_queue(self, nodes: list) -> None:
        """Add every node to the queue, then bubble to make it a heap"""
        self.distances = [None] * len(nodes)
        self.heap_map = [None] * len(nodes)
        for node in nodes:
            self.heap.append(node)
            self.heap_map[node.node_id] = len(self.heap) - 1
        for node in self.heap[::-1]:
            self.bubble_up(node)

    def insert(self, node: CS312GraphNode) -> None:
        self.heap.append(node)
        self.heap_map[node.node_id] = len(self.heap) - 1
        self.bubble_up(node)
    
    def bubble_up(self, node: CS312GraphNode) -> None:
        """Bring the node up the heap until it is larger than its parent"""
        parent = self.get_parent(node)
        if parent is not None and node.distance < parent.distance:
            self.swap(node, parent)
            self.bubble_up(node)
    
    def swap(self, first, second) -> None:
        """Swap the positions of two edges in the heap"""
        # get locations
        first_index = self.heap_map[first.node_id]
        second_index = self.heap_map[second.node_id]
        # heap swap
        self.heap[first_index] = second
        self.heap[second_index] = first
        # new locations
        self.heap_map[first.node_id] = second_index
        self.heap_map[second.node_id] = first_index

    def get_children(self, node: CS312GraphNode) -> tuple:
        """Get this node's children"""
        parent_index = self.heap_map[node.node_id]
        firstborn_index = parent_index * 2 + 1
        secondborn_index = parent_index * 2 + 2
        if firstborn_index >= len(self.heap):
            return None, None
        if secondborn_index >= len(self.heap):
            return self.heap[firstborn_index], None
        return self.heap[firstborn_index], self.heap[secondborn_index]

    def get_parent(self, node: CS312GraphNode) -> CS312GraphNode:
        """Get this node's parent"""
        node_index = self.heap_map[node.node_id]
        if node_index == 0:
            return None
        parent_index = (node_index - 1) // 2
        return self.heap[parent_index]

    def bubble_down(self, node: CS312GraphNode) -> None:
        """Bring the node down the heap until it is smaller than its children"""
        firstborn, secondborn = self.get_children(node)
        if firstborn is None:
            return
        if secondborn is None:
            if node.distance > firstborn.distance:
                self.swap(node, firstborn)
                self.bubble_down(node)
            return
        if firstborn.distance < secondborn.distance:
            if node.distance > firstborn.distance:
                self.swap(node, firstborn)
                self.bubble_down(node)
        else:
            if node.distance > secondborn.distance:
                self.swap(node, secondborn)
                self.bubble_down(node)

    def delete_min(self) -> CS312GraphNode:
        """Remove the smallest node, switch the end node to the top, and bubble it down"""
        if self.is_empty():
            return None
        
        min_node = self.heap[0]
        self.heap_map[min_node.node_id] = None

        if len(self.heap) == 1:
            return self.heap.pop()

        last_node = self.heap.pop()
        self.heap[0] = last_node
        self.heap_map[last_node.node_id] = 0
        self.bubble_down(last_node)
        return min_node

    def decrease_key(self, node: CS312GraphNode, new_distance) -> None:
        """Decrease the key of the node and bubble it up"""
        node.length = new_distance
        self.bubble_up(node)


