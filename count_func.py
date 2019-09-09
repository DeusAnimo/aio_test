from models import session, Medias


def red_count(account_id, tag, red_gt):
    if tag is not None:
        counts = session.query(Medias).filter(
            Medias.red > red_gt,
            Medias.account_id == account_id,
            Medias.tag == tag
        ).count()
        return counts
    counts = session.query(Medias).filter(
        Medias.red > red_gt,
        Medias.account_id == account_id
    ).count()
    return counts
