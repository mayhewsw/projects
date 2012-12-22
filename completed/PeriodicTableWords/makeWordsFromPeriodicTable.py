#! /usr/bin/python3

with open('/usr/share/dict/words', 'r') as f:
    words = f.readlines()

# Remove newline
words = list(map(lambda s: s.strip(), words))
words = list(filter(lambda s: len(s) > 0, words))

pt = ("Ac",  "Ag",  "Al",  "Am",  "Ar",  "As",  "At",  "Au",  "B",  "Ba",  "Be",  "Bh",  "Bi",  "Bk",  "Br",  "C",  "Ca",  "Cd",  "Ce",  "Cf",  "Cl",  "Cm",  "Co",  "Cn",  "Cr",  "Cs",  "Cu",  "Db",  "Ds",  "Dy",  "Er",  "Es",  "Eu",  "F",  "Fe",  "Fm",  "Fr",  "Ga",  "Gd",  "Ge",  "H",  "He",  "Hf",  "Hg",  "Ho",  "Hs",  "I",  "In",  "Ir",  "K",  "Kr",  "La",  "Li",  "Lr",  "Lu",  "Md",  "Mg",  "Mn",  "Mo",  "Mt",  "N",  "Na",  "Nb",  "Nd",  "Ne",  "Ni",  "No",  "Np",  "O",  "Os",  "P",  "Pa",  "Pb",  "Pd",  "Pm",  "Po",  "Pr",  "Pt",  "Pu",  "Ra",  "Rb",  "Re",  "Rf",  "Rg",  "Rh",  "Rn",  "Ru",  "S",  "Sb",  "Sc",  "Se",  "Sg",  "Si",  "Sm",  "Sn",  "Sr",  "Ta",  "Tb",  "Tc",  "Te",  "Th",  "Ti",  "Tl",  "Tm",  "U",  "Uuh",  "Uun",  "Uuo",  "Uup",  "Uuq",  "Uus",  "Uut",  "Uuu",  "V",  "W",  "Xe",  "Y",  "Yb",  "Zn",  "Zr")

# Make all lower case
pt = list(map(lambda s: s.lower(), pt))


# Prob fastest to run through dictionary and tell if is possible to do stuff
#mywords = ["bacon", "heat", "bar", "mayhew", "uunuuo"]
finalWords = {}

for w in words:
    # can I make w using pt?
    # Begin at the beginning, if any pairs match, then so be it, try all possibilities.
    w = w.lower()

    candidates = [w]
    d = {w:[]}

    for c in candidates:
        # For safety's sake
        if len(c) == 0:
            continue

        # Is the first character in there?
        if c[0] in pt:
            if len(c) == 1:
                finalWords[w] = d[c]+ [c]
                break # continue?
            candidates.append(c[1:])
            d[c[1:]] = d[c] + [c[0]]

        # Are the first two?
        if c[0:2] in pt:
            if len(c) == 2:
                finalWords[w] = d[c] + [c]
                break # continue?
            candidates.append(c[2:])
            d[c[2:]] = d[c] + [c[:2]]
                        
        # The first three?
        if c[0:3] in pt:
            if len(c) == 3:
                finalWords[w] = d[c] + [c]
                break
            candidates.append(c[3:])
            d[c[3:]] = d[c]+ [c[:3]]



with open("allposs.txt", "w") as out:
    keys = sorted(finalWords.keys())
    
    for k in keys:
        out.write(k.capitalize() + ": ")
        for s in finalWords[k]:
            out.write(s.capitalize() + " ")
        out.write("\n")

    
    
    


