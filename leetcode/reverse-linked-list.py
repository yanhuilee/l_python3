# 题号：206
# 反转链表


class ListNode:
    # Definition for singly-linked list.
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        cur, next = head, None
        while cur:
            cur.next, prev, cur = prev, cur, cur.next
            print(cur.val, prev.val)
        return prev


if __name__ == '__main__':
    list = [1, 2, 3, 4, 5]
    head = ListNode(list[0])
    cur = head
    for i in range(1, len(list)):
        node = ListNode(list[i])
        cur.next = node
        cur = node
    # while head:
    #     print(head.val, head.next)
    #     head = head.next
    solution = Solution()
    reverse = solution.reverseList(head)
    while reverse:
        print(reverse.val, reverse.next)
        reverse = reverse.next

