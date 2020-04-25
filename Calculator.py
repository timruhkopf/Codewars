class Calculator(object):
    # https://www.codewars.com/kata/5235c913397cbf2508000048
    
    def evaluate(self, string):
        interval_string = string.split(' ')
        interval_string = self.calculate(interval_string, ['*','/'])
        return float(self.calculate(interval_string, ['+','-'])[0])

    @staticmethod
    def calculate(interval_string, operator):

        operation = {'*': lambda x, y: x * y,
                     '/': lambda x, y: x / y,
                     '+': lambda x, y: x + y,
                     '-': lambda x, y: x - y}
        new_list = []

        for i, j in enumerate(interval_string):
            if j == operator[0] or j == operator[1]:
                new_list.append(operation[j](float(new_list[-1]), float(interval_string[i + 1])))
                new_list.pop(-2)
                interval_string.pop(i + 1)
            else:
                new_list.append(j)

        return new_list

if __name__ == '__main__':
    Calculator().evaluate("2 / 2 + 3 * 4 - 6") == 7
