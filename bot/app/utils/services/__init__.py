class Services:
    ALL_SERVICES = set()
    UNMUTED = set()
    MUTED = set()
    LATEST = ''


def add_latest(name):
    Services.LATEST = name


def add(name):
    Services.ALL_SERVICES.add(name)
    Services.UNMUTED.add(name)
    add_latest(name)


def remove(name):
    try:
        Services.ALL_SERVICES.remove(name)
        Services.UNMUTED.remove(name)
        Services.MUTED.remove(name)
    except Exception:
        pass


def mute(name):
    if name in Services.ALL_SERVICES:
        try:
            Services.MUTED.add(name)
            Services.UNMUTED.remove(name)
        except Exception:
            pass


def unmute(name):
    try:
        Services.MUTED.remove(name)
        Services.UNMUTED.add(name)
    except Exception:
        pass


def show_muted():
    muted_list = ''
    for service in Services.MUTED:
        muted_list += '- {}\n'.format(service)
    return muted_list


def show_unmuted():
    unmuted_list = ''
    for service in Services.UNMUTED:
        unmuted_list += '- {}\n'.format(service)
    return unmuted_list


def show_all():
    all_list = ''
    for service in Services.ALL_SERVICES:
        if service in Services.MUTED:
            all_list += '- {}\t🤫\n'.format(service)
        elif service in Services.UNMUTED:
            all_list += '- {}\t😬\n'.format(service)
    return all_list


def is_muted(name):
    if name in Services.MUTED:
        return True
    return False


def mute_latest():
    mute(Services.LATEST)


def unmute_latest():
    unmute(Services.LATEST)


def unmute_all():
    for service in Services.MUTED:
        unmute(service)


def clear():
    Services.ALL_SERVICES = set()
    Services.MUTED = set()
    Services.UNMUTED = set()
