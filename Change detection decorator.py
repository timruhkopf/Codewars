
def change_detection(Cls):

    class NewCls(object):
        def __init__(self, *args, **kwargs):
            Cls.__init__(self, *args, **kwargs)

    cls = NewCls
    return cls


@change_detection
class Struct:
    def __init__(self, y, x):
        self.y = y
        self.x = x


a  = Struct(1,2)























