# get the mean avergae error of two independent vectors

# example arrays
array_a = [1,2,3,4,5]
array_b = [5,4,3,2,1]


def solution(array_a, array_b):
    return sum((a - b)**2 for a, b in zip(array_a, array_b)) / len(array_a)


