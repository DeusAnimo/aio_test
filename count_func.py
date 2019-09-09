from models import session, Medias


def red_count(account_id, tag, red_gt):
    if tag and account_id is not None:
        counts = session.query(Medias).filter(
            Medias.red > red_gt,
            Medias.account_id == account_id,
            Medias.tag == tag
        ).count()
        return counts
    elif account_id:
        counts = session.query(Medias).filter(
            Medias.red > red_gt,
            Medias.account_id == account_id
        ).count()
        return counts
    elif tag:
        counts = session.query(Medias).filter(
            Medias.red > red_gt,
            Medias.tag == tag
        ).count()
        return counts
    counts = session.query(Medias).filter(
        Medias.red > red_gt
    ).count()
    return counts
