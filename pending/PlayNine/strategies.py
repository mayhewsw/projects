# a strategy looks like this:


def ignore(card, cardisvisible, mycards):
    """
    In this strategy, draw a card and ignore it. The extra arguments are
    needed so that player.wrap() works correctly.
    """
    return card


def firstempty(card, cardisvisible, mycards):
    """
    Put this card in the first empty spot.
    """
    discard = False
    for v, c in zip(cardisvisible, mycards):
        if v[0] == "?":
            v[0] = card
            discard = c[0]
            c[0] = card
            break
        elif v[1] == "?":
            v[1] = card
            discard = c[1]
            c[1] = card
            break
    return discard


def findpair(card, cardisvisible, mycards):
    """
    If this card makes a pair anywhere, include it.
    """
    discard = False
    for v, c in zip(cardisvisible, mycards):
        if v[1] == card and v[0] != card:
            # replace c[0] and v[0]
            v[0] = card
            discard = c[0]
            c[0] = card
            break
        elif v[0] == card and v[1] != card:
            # replace c[1] and v[1]
            v[1] = card
            discard = c[1]
            c[1] = card
            break
    return discard


def lowerscore(card, cardisvisible, mycards):
    """
    if there is a mismatched pair (including one unknown), replace
    a card if it is larger than the card c
    """
    discard = False
    for v, c in zip(cardisvisible, mycards):
        # if there is a pair, ignore it
        if v[0] == v[1]:
            continue
        if v[0] != "?" and card < v[0]:
            discard = v[0]
            c[0] = card
            v[0] = card
            break
        if v[1] != "?" and card < v[1]:
            discard = v[1]
            c[1] = card
            v[1] = card
            break
    return discard


def flipfirstunopened(card, cardisvisible, mycards):
    """
    just open up the first unopened one
    """
    for v, c in zip(cardisvisible, mycards):
        if v[0] == "?":
            v[0] = c[0]
            break
        elif v[1] == "?":
            v[1] = c[1]
            break
    return card