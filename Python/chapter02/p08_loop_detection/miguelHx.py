"""
Python version 3.7.0
2.8 - Loop Detection
Given a circular linked list, implement an algorithm that
returns the node at the beginning of the loop.
DEFINITION
Circular linked list: A (corrupt) linked list in which
a node's next pointer points to an earlier node, so as
to make a loop in the linked list.
EXAMPLE
Input:  A -> B -> C -> D -> E -> C [the same C as earlier]
Output:  C
"""
import unittest
from typing import Optional, NamedTuple


class Node:
    def __init__(self, d: int):
        self.data = d
        self.next = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<Node Value: {}>'.format(self.data)

    def __eq__(self, other: object):
        if not isinstance(other, Node):
            return NotImplemented
        return self.data == other.data

    def __hash__(self):
        """
        Hash based on node's memory address.
        :return:
        """
        return id(self)


class LinkedList:
    def __init__(self, *numbers: int):
        self.head = None
        self.tail = None
        self.size = 0
        for num in numbers:
            self.append_to_tail(num)

    def append_to_tail(self, e) -> None:
        if isinstance(e, int):
            self._append_num(e)
        elif isinstance(e, Node):
            self._append_node(e)

    def _append_num(self, d: int) -> None:
        if self.head is None:
            self.head = Node(d)
            self.tail = self.head
        else:
            end = Node(d)
            self.tail.next = end
            self.tail = end
        self.size += 1

    def _append_node(self, n: Node) -> None:
        if self.head is None:
            self.head = n
            self.tail = self.head
        else:
            end = n
            self.tail.next = end
            self.tail = end
        self.size += 1

    def append_to_head(self, d: int) -> None:
        new_head = Node(d)
        new_head.next = self.head
        if self.head is None:
            # if list is empty and we add
            # out first element, head AND tail
            # must point to same node
            self.tail = new_head
        self.head = new_head
        self.size += 1

    def get_node_at(self, index: int) -> Node:
        if index < 0 or index >= self.size:
            raise IndexError('list index out of range')
        n = self.head
        for i in range(self.size):
            if i == index:
                return n
            n = n.next

    def get_value_at(self, index: int) -> int:
        if index < 0 or index >= self.size:
            raise IndexError('list index out of range')
        n = self.head
        for i in range(self.size):
            if i == index:
                return n.data
            n = n.next

    def pop_head(self) -> Node:
        if self.head is None:
            raise IndexError('no head to pop')
        h = self.head
        h.next = None
        self.head = self.head.next
        self.size -= 1
        return h

    def append(self, ll: 'LinkedList') -> None:
        self.tail.next = ll.head
        self.tail = ll.tail
        self.size += ll.size
        ll.head = None
        ll.size = 0

    def reverse(self) -> None:
        """
        Reverses this linked list in place
        :return:
        """
        if self.head is None:
            return
        prev = self.head
        self.tail = prev
        curr = prev.next
        self.tail.next = None
        while curr is not None:
            old_next = curr.next
            curr.next = prev
            prev = curr
            curr = old_next
        self.head = prev

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.head is None:
            return '<empty>'
        ll = []
        n = self.head
        while n.next is not None:
            ll.append('{} -> '.format(n.data))
            n = n.next
        ll.append(str(n.data))
        return ''.join(ll)

    def __eq__(self, other: object):
        if not isinstance(other, LinkedList):
            return NotImplemented
        a = self.head
        b = other.head
        while a is not None and b is not None:
            if a.data != b.data:
                return False
            # otherwise, advance both pointers
            a = a.next
            b = b.next
        return a is None and b is None


def loop_detection_linear_time_const_space(ll: LinkedList):
    """
    This function will determine if there is a
    cycle in the input linked list.
    A linked list is 'circular' when a node's
    next pointer points to an earlier node, so
    as to make a loop in the linked list.
    Floyd cycle-finding algorithm:
        https://www.geeksforgeeks.org/detect-loop-in-a-linked-list/
    Runtime:  O(n)
    Space Complexity:  O(1)
    :param ll: an input linked list
    :return: the corrupt node or None
    """
    # for the case of a linked list with
    # a single node, non-corrupt
    if ll.head and ll.head.next is None:
        return None
    slow_ptr = ll.head
    fast_ptr = ll.head
    while slow_ptr and fast_ptr and fast_ptr.next:
        slow_ptr = slow_ptr.next
        fast_ptr = fast_ptr.next.next
        if fast_ptr.next is None:
            return None
        if slow_ptr is fast_ptr:
            # we have a cycle
            break
    # if we get here, then there is a cycle.
    # advance one of fast or slow pointers
    # and a pointer that starts in the
    # beginning, by one until they match.
    # they will end at the beginning of
    # the cycle.
    p = ll.head
    while p is not slow_ptr:
        p = p.next
        slow_ptr = slow_ptr.next
    return p


def loop_detection_const_space(ll: LinkedList) -> Optional[Node]:
    """
    This function will determine if there is a
    cycle in the input linked list.
    A linked list is 'circular' when a node's
    next pointer points to an earlier node, so
    as to make a loop in the linked list.
    Runtime:  O(n^2)
    Space Complexity:  O(1)
    :param ll: an input linked list
    :return: the corrupt node or None
    """
    # for the case of a single-node corrupt linked list
    if ll.head and ll.head.next is ll.head:
        return ll.head
    # this algorithm will traverse through the
    # linked list, and at each element, we will loop from
    # the start up to the current node, comparing
    # the next pointer of the current node with
    # each node leading up to the current node
    curr_node = ll.head
    while curr_node is not None:
        n = ll.head  # n is a node
        # we will be traversing 'n' up to the current node
        # to see if a previous node happens to be the
        # 'next' of the current node.
        while n is not curr_node:
            if curr_node.next is n:
                # cycle found
                return n
            n = n.next
        curr_node = curr_node.next
    return None


def loop_detection(ll: LinkedList) -> Optional[Node]:
    """
    This function will determine if there is a
    cycle in the input linked list.
    A linked list is 'circular' when a node's
    next pointer points to an earlier node, so
    as to make a loop in the linked list.
    Runtime:  O(n)
    Space Complexity:  O(n)
    :param ll: an input linked list
    :return: the corrupt node or None
    """
    nodes_seen = set()
    n = ll.head
    while n is not None:
        if n in nodes_seen:
            return n
        nodes_seen.add(n)
        n = n.next
    return None


class CorruptLLStructure(NamedTuple):
    first_segment: LinkedList
    second_segment: LinkedList
    corrupt_node: Node


class TestLoopDetection(unittest.TestCase):

    def setUp(self):
        corrupt_structures = [
            CorruptLLStructure(
                LinkedList(1, 2),
                LinkedList(4, 5),
                Node(3)
            ),
            CorruptLLStructure(
                LinkedList(1),
                LinkedList(3),
                Node(2)
            ),
            CorruptLLStructure(
                LinkedList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
                LinkedList(13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23),
                Node(12)
            ),
            CorruptLLStructure(
                LinkedList(1, 2, 3, 4, 5),
                LinkedList(7, 8, 9),
                Node(6)
            ),
            CorruptLLStructure(
                LinkedList(),
                LinkedList(2, 3, 4, 5, 6, 7, 8, 9),
                Node(1)
            ),
            CorruptLLStructure(
                LinkedList(1),
                LinkedList(3, 4, 5, 6, 7, 8, 9),
                Node(2)
            )
        ]
        self.loop_detection_test_cases = []
        for s in corrupt_structures:
            s.first_segment.append_to_tail(s.corrupt_node)
            s.first_segment.append(s.second_segment)
            s.first_segment.tail.next = s.corrupt_node
            self.loop_detection_test_cases.append((s.first_segment, s.corrupt_node))

    def test_loop_detection(self):
        for ll, corrupt_node in self.loop_detection_test_cases:
            self.assertEqual(loop_detection(ll), corrupt_node)
            self.assertEqual(loop_detection_const_space(ll), corrupt_node)
            self.assertEqual(loop_detection_linear_time_const_space(ll), corrupt_node)

    def test_loop_detection_single_node_ll(self):
        ll = LinkedList()
        ll.append_to_tail(1)
        corrupt_node = ll.head
        ll.head.next = corrupt_node
        self.assertEqual(loop_detection(ll), corrupt_node)
        self.assertEqual(loop_detection_const_space(ll), corrupt_node)
        self.assertEqual(loop_detection_linear_time_const_space(ll), corrupt_node)

    def test_loop_detection_empty_ll(self):
        ll = LinkedList()
        self.assertIsNone(loop_detection(ll))
        self.assertIsNone(loop_detection_const_space(ll))
        self.assertIsNone(loop_detection_linear_time_const_space(ll))

    def test_loop_detection_non_corrupt_ll(self):
        for ll in [
            LinkedList(1, 2, 3, 4, 5),
            LinkedList(1),
            LinkedList()
        ]:
            self.assertIsNone(loop_detection(ll))
            self.assertIsNone(loop_detection_const_space(ll))
            self.assertIsNone(loop_detection_linear_time_const_space(ll))


if __name__ == '__main__':
    unittest.main()
