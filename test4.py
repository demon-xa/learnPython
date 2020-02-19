# BEGIN (write your solution here)
def sort_pair(a):
    if a[0] > a[1]:
        return (a[1], a[0])
    return a
# END


print(sort_pair((2, 2)))