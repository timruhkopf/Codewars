class Dictionary(dict):
    def newentry(self, word, definition):
        self[word] = definition

    def look(self, key):
        return self[key] if key in self.keys() else "Can't find entry for {}".format(key)


if __name__ == '__main__':
    d = Dictionary()

    d.newentry("Apple", "A fruit")
    Test.assert_equals(d.look("Apple"), "A fruit")

    d.newentry("Soccer", "A sport")
    Test.assert_equals(d.look("Soccer"), "A sport")
    Test.assert_equals(d.look("Hi"), "Can't find entry for Hi")
    Test.assert_equals(d.look("Ball"), "Can't find entry for Ball")

    d.newentry("soccer", "a sport")
    Test.assert_equals(d.look("soccer"), "a sport")
