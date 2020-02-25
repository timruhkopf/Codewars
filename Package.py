
class Package(object):
    """Challenge @ https://www.codewars.com/kata/587e1ef6f1a2534bbe0001ef"""

    def __init__(self, length, width, height, weight):
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
        self.__setattr__('volume', 0)

    def __setattr__(self, key, value):
        bounds = {'length': (0, 350), 'width': (0, 300), 'height': (0, 150), 'weight': (0, 40)}
        if key in bounds.keys():
            lower, upper = bounds[key]

            if (value < lower) | (upper < value):
                raise DimensionsOutOfBoundError(key, value, lower, upper)

        object.__setattr__(self, key, value)

    def volume(self):
        return self.volume
    @volume.getter
    def volume(self):
        return self.length * self.width * self.height


class DimensionsOutOfBoundError(Exception):
    def __init__(self, variable, value, lower, upper):
        s = "Package {variable}=={value} out of bounds, " \
            "should be: {lower} < {variable} <= {upper}".format(
            variable=variable, value=value, lower=lower, upper=upper)
        Exception.__init__(self, s)


if __name__ == '__main__':
    from Test_Codewars import test

    test.describe("Basic tests")
    test.it("Building packages with allowed dimensions")
    allowed_inputs = [
        [20, 30, 10, 10],
        [0.2, 0.2, 0.2, 0.02],
        [350, 300, 150, 40],
        [99, 99, 99, 40]
    ]
    for inp in allowed_inputs:
        p = Package(*inp)
        test.assert_equals(p.length, inp[0])
        test.assert_equals(p.width, inp[1])
        test.assert_equals(p.height, inp[2])
        test.assert_equals(p.weight, inp[3])

    test.it("Setting package variables to allowed values")
    inputs = (0.2, 0.2, 0.2, 0.2)
    p = Package(*inputs)
    p.length = 2
    test.assert_equals(p.length, 2)
    p.width = 100
    test.assert_equals(p.width, 100)
    p.height = 149
    test.assert_equals(p.height, 149)
    p.weight = 40
    test.assert_equals(p.weight, 40)

    test.it("Setting package variables to disallowed values")
    inputs = (0.2, 0.2, 0.2, 0.2)
    p = Package(*inputs)
    try:
        p.length = -20
        test.assert_equals(True, False, "Should have raised DimensionsOutOfBoundError")

    except DimensionsOutOfBoundError as e:
        test.assert_equals(str(e), "Package length==-20 out of bounds, should be: 0 < length <= 350")
    try:
        p.length = 2000
        test.assert_equals(True, False, "Should have raised DimensionsOutOfBoundError")

    except DimensionsOutOfBoundError as e:
        test.assert_equals(str(e), "Package length==2000 out of bounds, should be: 0 < length <= 350")

    try:
        p.width = -20
        test.assert_equals(True, False, "Should have raised DimensionsOutOfBoundError")
    except DimensionsOutOfBoundError as e:
        test.assert_equals(str(e), "Package width==-20 out of bounds, should be: 0 < width <= 300")
    try:
        p.width = 2000
        test.assert_equals(True, False, "Should have raised DimensionsOutOfBoundError")

    except DimensionsOutOfBoundError as e:
        test.assert_equals(str(e), "Package width==2000 out of bounds, should be: 0 < width <= 300")

    try:
        p.height = -20
        test.assert_equals(True, False, "Should have raised DimensionsOutOfBoundError")
    except DimensionsOutOfBoundError as e:
        test.assert_equals(str(e), "Package height==-20 out of bounds, should be: 0 < height <= 150")
    try:
        p.height = 2000
        test.assert_equals(True, False, "Should have raised DimensionsOutOfBoundError")

    except DimensionsOutOfBoundError as e:
        test.assert_equals(str(e), "Package height==2000 out of bounds, should be: 0 < height <= 150")

    try:
        p.weight = -20
        test.assert_equals(True, False, "Should have raised DimensionsOutOfBoundError")
    except DimensionsOutOfBoundError as e:
        test.assert_equals(str(e), "Package weight==-20 out of bounds, should be: 0 < weight <= 40")
    try:
        p.weight = 2000
        test.assert_equals(True, False, "Should have raised DimensionsOutOfBoundError")

    except DimensionsOutOfBoundError as e:
        test.assert_equals(str(e), "Package weight==2000 out of bounds, should be: 0 < weight <= 40")

    test.it("Building packages with disallowed length values")
    try:
        p = Package(*[-20, 30, 10, 10])
        test.assert_equals(True, False, "Should have raised DimensionsOutOfBoundError")
    except DimensionsOutOfBoundError as e:
        test.assert_equals(str(e), "Package length==-20 out of bounds, should be: 0 < length <= 350")

    try:
        p = Package(*[351, 30, 10, 10])
        test.assert_equals(True, False, "Should have raised DimensionsOutOfBoundError")
    except DimensionsOutOfBoundError as e:
        test.assert_equals(str(e), "Package length==351 out of bounds, should be: 0 < length <= 350")

    test.it("Building packages with disallowed width values")
    try:
        p = Package(*[20, -30, 10, 10])
        test.assert_equals(True, False, "Should have raised DimensionsOutOfBoundError")
    except DimensionsOutOfBoundError as e:
        test.assert_equals(str(e), "Package width==-30 out of bounds, should be: "
                                   "0 < width <= 300")

    try:
        p = Package(*[20, 301, 10, 10])
        test.assert_equals(True, False, "Should have raised DimensionsOutOfBoundError")
    except DimensionsOutOfBoundError as e:
        test.assert_equals(str(e), "Package width==301 out of bounds, should be: "
                                   "0 < width <= 300")

    test.it("Building packages with disallowed height values")
    try:
        p = Package(*[20, 30, -10, 10])
        test.assert_equals(True, False, "Should have raised DimensionsOutOfBoundError")
    except DimensionsOutOfBoundError as e:
        test.assert_equals(str(e), "Package height==-10 out of bounds, should be: 0 < height <= 150")

    try:
        p = Package(*[20, 10, 151, 10])
        test.assert_equals(True, False, "Should have raised DimensionsOutOfBoundError")
    except DimensionsOutOfBoundError as e:
        test.assert_equals(str(e), "Package height==151 out of bounds, should be: 0 < height <= 150")

    test.it("Accessing volume")
    p = Package(10, 12, 13, 20)
    test.assert_equals(p.volume, 10 * 12 * 13)
    p.length = 24
    test.assert_equals(p.volume, 24 * 12 * 13)
