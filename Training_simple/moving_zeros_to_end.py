def move_zeros(array):
    # https://www.codewars.com/kata/52597aa56021e91c93000cb0
    return sorted(array, key=lambda x: x == 0 and x is not False)

if __name__ == '__main__':
    array = [False,1,0,1,2,0,1,3,"a"]
    move_zeros(array) == [False,1,1,2,1,3,"a",0,0]
