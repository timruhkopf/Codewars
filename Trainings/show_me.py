def show_me(instname):
    """
    Challenge @ https://www.codewars.com/kata/561f9d37e4786544e0000035/
    :param instname:
    :return: string
    """
    key = sorted(instname.__dict__.keys())

    s = "Hi, I'm one of those {}s! Have a look at my {}.".format(instname.__class__.__name__, key[0])
    s2 = s[:-1] + ', {} and {}.'.format(', '.join(key[1:-1]), key[-1])

    return (s, s2)[len(key) > 1]


if __name__ == '__main__':
    from Test_Codewars import test

    test.describe("Testing for instance porsche of class Vehicle...")


    class Vehicle:
        def __init__(self, seats, wheels, engine):
            self.seats = seats
            self.wheels = wheels
            self.engine = engine


    porsche = Vehicle(2, 4, 'Gas')
    test.assert_equals(show_me(porsche), "Hi, I'm one of those Vehicles! Have a look at my engine, seats and wheels.")

    test.describe("Testing for instance earth of Planet...")


    class Planet:
        def __init__(self, moon):
            self.moon = moon


    earth = Planet('moon')
    test.assert_equals(show_me(earth), "Hi, I'm one of those Planets! Have a look at my moon.")
