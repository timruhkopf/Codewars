def alphabet_war(reinforces, airstrikes):
    '''
    Task
    Write a function that accepts reinforces array of strings and airstrikes
    array of strings. The reinforces strings consist of only small letters.
    The size of each string in reinforces array is the same. The airstrikes
    strings consists of * and white spaces. The size of each airstrike may vary.
    There may be also no airstrikes at all.

    The first row in reinforces array is the current battlefield. Whenever some
    letter is killed by bomb, it's replaced by a letter from next string in
    reinforces array on the same position. The airstrike always starts from the
    beginning of the battlefield. The * means a bomb drop place. The each * bomb
    kills letter only on the battelfield. The bomb kills letter on the same
    index on battlefield plus the adjacent letters. The letters on the
    battlefield are replaced after airstrike is finished. Return string of
    letters left on the battlefield after the last airstrike. In case there is
    no any letter left in reinforces on specific position, return _.

    :param reinforces: list of strings with letters
    :param airstrikes: list of strings with spaces & stars
    :return: 'output string'
    '''
    def devastation(airstrike):
        return {i + a for i, v in enumerate(airstrike) for a in range(-1, 2) if v == '*'}

    # flatten list of strike indices.
    bombindex = [item for sublist in map(devastation, airstrikes) for item in sublist
                 if (item >= 0 & item <= len(reinforces[0]))]  # clean up dirty bomb ;)

    # frequency of explosions at index position
    frequency = [bombindex.count(i) for i in range(len(reinforces[0]))]

    # create result letter by letter with frequency as index on reinforcement
    result = [reinforces[v][i] if (v < len(reinforces)) else '_'
              for i, v in enumerate(frequency)]

    return ''.join(result)


if __name__ == '__main__':
    alphabet_war(reinforces=
                 ["g964xxxxxxxx",
                  "myjinxin2015",
                  "steffenvogel",
                  "smile67xxxxx",
                  "giacomosorbi",
                  "freywarxxxxx",
                  "bkaesxxxxxxx",
                  "vadimbxxxxxx",
                  "zozofouchtra",
                  "colbydauphxx"],
                 airstrikes=
                 ["* *** ** ***",
                  " ** * * * **",
                  " * *** * ***",
                  " **  * * ** ",
                  "* ** *   ***",
                  "***   ",
                  "**",
                  "*",
                  "*"])
