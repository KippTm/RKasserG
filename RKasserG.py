import pdfplumber
import pandas as pd
import sys

def from_danish(number_str):
    """Convert a Danish number format string to a float."""
    return float(number_str.replace('.', '').replace(',', '.'))

def check_carls(lines):
    # keywords per category
    categories = {
        'Cider': ['Somersby'],
        'Øl': [],
        'Fadøl': ['Modular'],
        'Vand': ['Coca-Cola', 'Fanta', 'Schweppes', 'Craft', 'Squash'],
        'Energi': ['Monster'],
        'Pant': ['Flaskepant', 'ks', 'Euro', 'Master'],  # Handled separately with "Subtotal" + "emballage"
    }

    totals = {name: 0.0 for name in categories}
    pant = 0.0
    
    for l in lines:
        parts = l.split()
        match_found = ""
        # value is the second-to-last token (before potential currency)
        value_token = parts[-2] if len(parts) >= 2 else "0,00"
        
        # Check regular categories
        for name, kws in categories.items():
            if any(any(kw in token for token in parts) for kw in kws):
                if match_found != "":
                    print("Found overlapping categories in line:", l)
                    print("Categories:", match_found, "and", name)
                else:
                    print(name, ": ", l)
                match_found += name + " "
                try:
                    totals[name] += from_danish(value_token)
                    print("Added", from_danish(value_token), "to", name)
                    print("New total for", name, "is", totals[name])
                except Exception:
                    # ignore parse errors for now
                    pass


    total = sum(totals.values())
    bilag = [[name, amt * 1.25] for name, amt in totals.items()]
    bilag.append(['Total', total * 1.25])
    return bilag

def check_drinx(lines):
    other = ["Pant", "Palle"]
    til = ["Istønde,", "Strips", "Pantsække,", "Appelsiner,", "Istang,", "Lime", "Mynte,", "Rørsukker,", "Sugerør,", "Monin", "Ponte", "t/fadølsanlæg"]
    mixer = ["Maté", "Sprite", "Schweppes", "Faxe", "Coca", "Pellegrino", "Sprite,"]
    booze = ["Vodka", "Baileys", "Gammel", "Bacardi", "Fugle", "Cuba", "Jägermeister#", "Gin", "Fernet-Branca", "Pisang", "Minttu", "Aperol", "Barmix", "Prosecco", "Tequila", "Passoa", "Råstoff", "Sambuca", "Havana"]
    energidrikke = ["Red", "Monster"]
    cid = ["Ice", "Somersby"]
    bee = ["Ceres", "Classic"]
    fustage = cider = tilbehør = spiritus = vand = energi = pant = miljøtillæg = beer = 0.0
    match_found = False
    for l in lines:
        parts = l.split()
        if any(p in booze for p in parts):
            if match_found:
                print("Found overlapping categories in line:", l)
            match_found = True
            spiritus += from_danish(parts[len(parts)-1])
        if any(p in mixer for p in parts):
            if match_found:
                print("Found overlapping categories in line:", l)
            match_found = True
            vand += from_danish(parts[len(parts)-1])
        if any(p in other for p in parts):
            if match_found:
                print("Found overlapping categories in line:", l)
            match_found = True
            pant += from_danish(parts[len(parts)-1])
        if any(p in energidrikke for p in parts):
            if match_found:
                print("Found overlapping categories in line:", l)
            match_found = True
            energi += from_danish(parts[len(parts)-1])
        if any(p in til for p in parts):
            if match_found:
                print("Found overlapping categories in line:", l)
            match_found = True
            tilbehør += from_danish(parts[len(parts)-1])
        if "Fustage" in parts and "Pant" not in parts:
            if match_found:
                print("Found overlapping categories in line:", l)
            match_found = True
            fustage += from_danish(parts[len(parts)-1])
        if any(p in cid for p in parts):
            if match_found:
                print("Found overlapping categories in line:", l)
            match_found = True
            cider += from_danish(parts[len(parts)-1])
        if any("Miljøtillæg" in p for p in parts):
            if match_found:
                print("Found overlapping categories in line:", l)
            match_found = True
            miljøtillæg += from_danish(parts[len(parts)-1])
        if any(p in bee for p in parts):
            if match_found:
                print("Found overlapping categories in line:", l)
            match_found = True
            beer += from_danish(parts[len(parts)-1])
        if match_found:
            print("Found line:", l)
        match_found = False

    total = tilbehør + spiritus + vand + energi + pant + fustage + cider + miljøtillæg + beer
    bilag = [['Tilbehør', tilbehør*1.25],['Spiritus', spiritus*1.25], ['Vand', vand*1.25],
             ['Energi', energi*1.25], ['Pant', pant*1.25],['Cider', cider*1.25],
             ['Fadøl', fustage*1.25], ['Miljøafgift', miljøtillæg*1.25], ['Øl', beer*1.25], ['Total', total*1.25]]
    return bilag
def check_carls_tilskud(lines):
    # keywords per category (lowercased checks)
    categories = {
        'ØL': ['FL', 'DS', 'FL.', 'Fl', 'Fl.'],
        'Cider': ['Cider/Fabs'],
        'Fadøl': ['Fad'],
        'Energidrik': ['Energy'],
        'Vand': ['CL'],
    }

    totals = {name: 0.0 for name in categories}
    for l in lines:
        parts = l.split()
        match_found = ""
        # value is expected as the last token (e.g. "-7,92")
        value_token = parts[-1] if parts else "0,00"
        for name, kws in categories.items():
            if any(any(kw in token for token in parts) for kw in kws):
                if match_found != "":
                    print("Found overlapping categories in line:", l)
                    print("Categories:", match_found, "and", name)
                else:
                    print("Matched category", name, "in line:", l)
                match_found += name + " "
                try:
                    totals[name] += from_danish(value_token)
                except Exception:
                    # ignore parse errors for now
                    pass
        if match_found:
            print("Found line:", l)

    total = sum(totals.values())
    bilag = [[name, amt * 1.25] for name, amt in totals.items()]
    bilag.append(['Total', total * 1.25])
    return bilag
def nemlig_bilag(lines):
    # keywords per category
    categories = {
        'Øl': ['Grøn'],
        'Fadøl': ['fustage'],
        'Cider': ['Somersby', 'Breezer'],
        'Spiritus': ['Baileys'],
        'Vand': ['Coca-Cola', 'Squash', 'kakaomælk'],
        'Mad': [],
        'Pant': ['Pant'],
        'Fragt': ['Fragt', 'Pakkegebyr'],
    }

    totals = {name: 0.0 for name in categories}
    for l in lines:
        parts = l.split()
        match_found = ""
        # value is expected as the last token
        value_token = parts[-1] if parts else "0,00"
        for name, kws in categories.items():
            if any(any(kw in token for token in parts) for kw in kws):
                if match_found != "":
                    print("Found overlapping categories in line:", l)
                    print("Categories:", match_found, "and", name)
                match_found += name + " "
                try:
                    totals[name] += from_danish(value_token)
                except Exception:
                    # ignore parse errors for now
                    pass
        if match_found:
            print("Found line:", l)

    total = sum(totals.values())
    bilag = [[name, amt] for name, amt in totals.items()]
    bilag.append(['Total', total])
    return bilag

def pdf_to_csv(pdfFile, output, arg):
    #flaske, fustage, cider, spiritus, pant, energi = 0.0
    with pdfplumber.open(pdfFile) as pdf:
        data = [['Kategori', 'Belød']] 
        for p in pdf.pages:
            text = p.extract_text()
            lines = text.split("\n")
            match arg:
                case "c":
                    out = check_carls(lines)
                    data += [dat for dat in out]
                case "d":
                    out = check_drinx(lines)
                    data += [dat for dat in out]
                case "cl":
                    out = check_carls_tilskud(lines)
                    data += [dat for dat in out]
                case "nem":
                    out = nemlig_bilag(lines)
                    data += [dat for dat in out]
                case _:
                    print("Type not supported.")
                    return

    frame = pd.DataFrame(data)
    frame.to_csv(output, index=False, header=False) 


if len(sys.argv) < 3 or len(sys.argv) > 3:
    print("Usage: python3 RKasserG.py [bilag type] [file path]")
else:
    place = sys.argv[1]
    file = sys.argv[2]
    output = file.replace(".pdf", ".csv")
    pdf_to_csv(file, output, place)
