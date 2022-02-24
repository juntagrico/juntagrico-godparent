def is_godparent(member):
    return hasattr(member, 'godparent')


def is_godchild(member):
    return hasattr(member, 'godchild')
