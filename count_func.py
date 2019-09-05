from models import session, Medias


def red_count(account_id, tag, red_gt):
    counts = session.query(Medias).filter(Medias.account_id == account_id, Medias.tag == tag)
    val = 0
    for count in counts:
        if count.red > red_gt:
            val += 1
    return val
