import json


def jsonattr(path):
    """https://www.codewars.com/kata/55b0fb65e1227b17d60000dc"""

    with open(path) as json_file:
        data = json.load(json_file)

    def class_rebuilder(cls):
        # Deprec working verison on its own , but more elegant below
        # class NewClass(cls):
        #     pass
        # for name, val in data.items():
        #     setattr(NewClass, name, val)
        #
        # return NewClass

        for name, val in data.items():
            setattr(cls, name, val)
        return cls

    return class_rebuilder


if __name__ == '__main__':
    data = {"foo": "bar", "an_int": 5, "this_kata_is_awesome": True}
    with open('../../.PyCharmCE2019.3/config/scratches/myClass.json', 'w') as outfile:
        json.dump(data, outfile)


    @jsonattr("../../.PyCharmCE2019.3/config/scratches/myClass.json")
    class MyClass:
        pass


    MyClass.foo == "bar"
    MyClass.an_int == 5
    MyClass.this_kata_is_awesome == True
