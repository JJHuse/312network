#!/usr/bin/python3


from CS312Graph import *
import time


class NetworkRoutingSolver:
    def __init__( self):
        self.prevs = []

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        curr_dest = destIndex
        while self.prevs[curr_dest] is not None:
            prev_index = self.prevs[curr_dest]
            precursor = self.network.nodes[prev_index]
            for edge in precursor.neighbors:
                if edge.dest.node_id == curr_dest:
                    path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
                    break
            curr_dest = prev_index

        path_edges = path_edges[::-1]
        dest = self.network.nodes[destIndex]
        return {'cost':dest.distance, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        self.prevs = self.dijkstra(srcIndex)
        t2 = time.time()
        return (t2 - t1)
    
    def dijkstra(self, srcIndex: int):
        """Iterative method to find the shortest path from srcIndex to all other nodes in the network"""
        prevs = [None] * len(self.network.nodes)

        priority_queue = array_heap()
        priority_queue.make_queue(self.network.nodes, srcIndex)

        while not priority_queue.is_empty():
            node = priority_queue.delete_min()
            past = node.distance
            for edge in node.neighbors:
                dest = edge.dest
                alt = past + edge.length

                if dest.distance == float('inf') or alt < dest.distance:
                    prevs[dest.node_id] = node.node_id
                    priority_queue.decrease_key(dest, alt)

        return prevs


class array_heap:
    def __init__(self):
        self.heap = []
        self.heap_map = []

    def is_empty(self) -> bool:
        """Returns True if the heap is empty, False otherwise"""
        return len(self.heap) == 0

    def make_queue(self, nodes: list, srcIndex) -> None:
        """Add every node to the queue, then bubble to make it a heap"""
        self.heap_map = [None] * len(nodes)

        for node in nodes:
            self.heap.append(node)
            self.heap_map[node.node_id] = len(self.heap) - 1
            node.distance = float('inf')
        
        source = nodes[srcIndex]
        self.swap(source, self.heap[0])
        source.distance = 0
        ### All infinity
        # for node in self.heap[::-1]:
        #     self.bubble_up(node)

    def insert(self, node: CS312GraphNode) -> None:
        """Add new node and bubble it up"""
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
        node.distance = new_distance
        self.bubble_up(node)


