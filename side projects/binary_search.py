# time complexity: O(log(n))
# space complexity:O(1)

def binary_search(lst, target):
    nums = sorted(lst)

    l = 0
    r = len(nums) - 1


    while l <= r:
        m = (l + r) // 2

        if target == nums[m]:
            return m
        elif target > nums[m]:
            l = m + 1

        elif target < nums[m]:
            r = m - 1

    return -1 

print(binary_search([3, 5, 7, 8, 9], 10))