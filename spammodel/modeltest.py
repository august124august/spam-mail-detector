import csv
import re
spam_woorden ={}
gewone_woorden = {}
spam_mails = 0
gewone_mails = 0
email = input("Voer je email in: ")
email_woorden = re.findall(r'\b\w+\b', email.lower())
gefiltreerde_woorden = []

skipwoorden = ["de", "het", "een", "en", "van", "in", "op", "te", "is", "dat", "die", "met", "voor", "aan", "als", "bij", "door", "om", "tot", "uit"]

for woord in email_woorden:
    if woord not in skipwoorden:
        gefiltreerde_woorden.append(woord)
email_woorden = gefiltreerde_woorden


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
print("Totaal spam woorden:", totaal_spam)
print("Totaal gewone woorden:", totaal_gewone)
alle_woorden = set(spam_woorden) | set(gewone_woorden)
aantal_alle_woorden = len(alle_woorden)

print("Aantal alle woorden:", aantal_alle_woorden)
totaal_mails = spam_mails + gewone_mails
voorafkans_spam = spam_mails / totaal_mails
voorafkans_gewoon = gewone_mails / totaal_mails
print("Voorafkans spam:", voorafkans_spam)
print("Voorafkans gewone mail:", voorafkans_gewoon)
score_spam = voorafkans_spam
score_gewoon = voorafkans_gewoon
for woord in email_woorden:
    kans_spam = (spam_woorden.get(woord, 0) + 1) / (totaal_spam + aantal_alle_woorden)
    kans_gewone = (gewone_woorden.get(woord, 0) + 1) / (totaal_gewone + aantal_alle_woorden)
    score_spam *= kans_spam
    score_gewoon *= kans_gewone
print(f"Score voor spam: {score_spam}")
print(f"Score voor gewone mail: {score_gewoon}")
totaal_score = score_spam + score_gewoon
percentage_spam = score_spam / totaal_score * 100
percentage_gewoon = score_gewoon / totaal_score * 100


print(f"Kans op spam: {percentage_spam:.2f}%")
print(f"Kans op gewone mail: {percentage_gewoon:.2f}%")