def is_godparent(member):
    return hasattr(member, 'godparent')


def is_godchild(member):
    return hasattr(member, 'godchild') and member.godchild.progress is not member.godchild.DONE


def was_godchild(member):
    return hasattr(member, 'godchild') and member.godchild.progress is member.godchild.DONE


def member_depot(member):
    if member.subscription_future:
        return member.subscription_future.future_depot or member.subscription_future.depot
    elif member.subscription_current:
        return member.subscription_current.future_depot or member.subscription_current.depot
    return None
