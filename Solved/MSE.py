def solution(array_a, array_b):
    return sum((a - b)**2 for a, b in zip(array_a, array_b)) / len(array_a)

if __name__ == '__main__':
    a = [1,2,3,4,5]
    b = [5,4,3,2,1]
    solution(a, b) == 8.0



