def format_duration(seconds):
    if seconds == 0: return ('now')

    dictionary = {1: '{}',
                  2: '{} and {}',
                  3: '{}, {} and {}',
                  4: '{}, {}, {} and {}',
                  5: '{}, {}, {}, {} and {}'}

    def smhdy(*args):
        if args[0] == 0:
            pass
        else:
            if args[0] == 1:
                return '1 {}'.format(args[1])
            else:
                return '{} {}s'.format(args[0], args[1])

    _ydhm = [31536000, 86400, 3600, 60]
    _names = ['year', 'day', 'hour', 'minute', 'second']

    year = seconds // _ydhm[0]
    day = (seconds - year * _ydhm[0]) // _ydhm[1]
    hour = (seconds - (year * _ydhm[0] + day * _ydhm[1])) // _ydhm[2]
    minute = (seconds - (year * _ydhm[0] + day * _ydhm[1] + hour * _ydhm[2])) // _ydhm[3]
    second = (seconds - (year * _ydhm[0] + day * _ydhm[1] + hour * _ydhm[2] + minute * _ydhm[3]))
    _amount = [year, day, hour, minute, second]

    os = [smhdy(x,y) for x,y in zip(_amount, _names)]
    os = [i for i in os if i != None]

    return dictionary[len(os)].format(*os)










