import tkinter as tk
import csv
import re

venster = tk.Tk()
venster.title("Spamfilter gusto")
venster.geometry("400x300")
vraag_label = tk.Label(venster, text="Voer je email in:", font=("Arial", 12), width=50, height=5)
vraag_label.pack()
invoer = tk.Entry(venster, width=50)
invoer.pack()
def controleer_email():
    email = invoer.get()
    email_woorden = re.findall(r'\b\w+\b', email.lower())
    gefiltreerde_woorden = []

    skipwoorden = ["de", "het", "een", "en", "van", "in", "op", "te", "is", "dat", "die", "met", "voor", "aan", "als", "bij", "door", "om", "tot", "uit"]

    for woord in email_woorden:
        if woord not in skipwoorden:
            gefiltreerde_woorden.append(woord)
    email_woorden = gefiltreerde_woorden

    spam_woorden = {}
    gewone_woorden = {}
    spam_mails = 0
    gewone_mails = 0

    with open("mail.csv", encoding="utf-8", newline="") as bestand:
        lezer = csv.DictReader(bestand)

        for mail in lezer:
            gefiltreerde_woorden2 = []
            woorden = re.findall(r'\b\w+\b', mail["tekst"].lower())
            for woord in woorden:
                if woord not in skipwoorden:
                    gefiltreerde_woorden2.append(woord)
            woorden = gefiltreerde_woorden2
            if mail["label"] == "spam":
                tellingen = spam_woorden
                spam_mails += 1
            else:
                tellingen = gewone_woorden
                gewone_mails += 1
            for woord in woorden:
                if woord in tellingen:
                    tellingen[woord] += 1
                else:
                    tellingen[woord] = 1

    totaal_spam = sum(spam_woorden.values())
    totaal_gewone = sum(gewone_woorden.values())
    alle_woorden = set(spam_woorden) | set(gewone_woorden)
    aantal_alle_woorden = len(alle_woorden)

    totaal_mails = spam_mails + gewone_mails
    voorafkans_spam = spam_mails / totaal_mails
    voorafkans_gewoon = gewone_mails / totaal_mails

    score_spam = voorafkans_spam
    score_gewoon = voorafkans_gewoon
    for woord in email_woorden:
        kans_spam = (spam_woorden.get(woord, 0) + 1) / (totaal_spam + aantal_alle_woorden)
        kans_gewone = (gewone_woorden.get(woord, 0) + 1) / (totaal_gewone + aantal_alle_woorden)
        score_spam *= kans_spam
        score_gewoon *= kans_gewone 
        totale_score = score_spam + score_gewoon
        procentage_spam = (score_spam / totale_score) * 100
        procentage_gewoon = (score_gewoon / totale_score) * 100
        vraag_label.config(text=f"kans op scam: {procentage_spam:.2f}%\nkans op gewone mail: {procentage_gewoon:.2f}%")
knop = tk.Button(venster, text="Controleer", command=controleer_email)
knop.pack()
venster.mainloop()