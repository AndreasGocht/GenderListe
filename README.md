# GenderListe

> This is a German Language-based Project. The README.md is therefore in German.

Kleines Python Skript, das aus gegeben Wortlisten ein MS Word kompatibles Wörterbuch mit gegenderten Wörtern generiert.

Beispiel:

"Arbeiter" wird zu "Arbeiter:innen", wenn ":" als Gendertrennzeichen geben wurde.

Die Basisliste `worttabelle.csv` basiert auf dem "Gendering-Wortkatalog Wien", und steht unter Creative Commons Namensnennung 4.0 International.
Leider enthält die orginal Liste von https://www.data.gv.at/katalog/dataset/stadt-wien_genderingwortkatalogderstadtwien ein paar " die das Parsing erschweren, welche in der hier vorliegenden Version entfernt wurden.

Eine kleine Auswahl an bereits generierten Wörterbüchern für MS Office gibt es unter https://github.com/AndreasGocht/GenderListe/releases.
Unter [Hinzufügen oder Bearbeiten von Wörtern in einem Rechtschreibwörterbuch](https://support.office.com/de-de/article/hinzuf%C3%BCgen-oder-bearbeiten-von-w%C3%B6rtern-in-einem-rechtschreibw%C3%B6rterbuch-56e5c373-29f8-4d11-baf6-87151725c0dc) ganz untern gibt es eine Anleitung, wie die Wörterbücher hinzugefügt werden können (Hinzufügen des Benutzerwörterbuchs eines Drittanbieters).
`fehler_woerter.txt` listet Worte auf, die nicht aus dem Gendering-Wortkatalog Wien aufgenommen werden konnten.

## Benutzung

```
usage: parse_wortliste_wien.py [-h] -g [GENDERSPERATOR] -b [BINNEN_I] [-o [GENDERING_WORTKATALOG_WIEN]] [-l [LISTE]]
                               [-i [IGNORE_LISTE]] [-w [WOERTERBUCH]] [-f [FEHLER_WOERTERBUCH]]

Ließt Gendering-Wortkatalog Wien, und schreibt ein Wordwörterbuch.

optional arguments:
  -h, --help            show this help message and exit
  -g [GENDERSPERATOR], --gendersperator [GENDERSPERATOR]
                        Genderzeichen
  -b [BINNEN_I], --binnen_i [BINNEN_I]
                        Binnen-I, [ja oder nein]
  -o [GENDERING_WORTKATALOG_WIEN], --gendering-wortkatalog-wien [GENDERING_WORTKATALOG_WIEN]
                        Gendering-Wortkatalog Wien
  -l [LISTE], --liste [LISTE]
                        Zusätzliche Liste mit Wörtern, die zu gendern sind, ein Wort pro Zeile
  -i [IGNORE_LISTE], --ignore-liste [IGNORE_LISTE]
                        Liste mit Wörtern, die zu ignorieren sind, ein Wort pro Zeile
  -w [WOERTERBUCH], --woerterbuch [WOERTERBUCH]
                        Wörterbuch Name zum Speichern
  -f [FEHLER_WOERTERBUCH], --fehler-woerterbuch [FEHLER_WOERTERBUCH]
                        Wörterbuch mit Wörtern, die nicht verarbeitet werden können
```

Besipiel:

```
python parse_wortliste_wien.py -g ":" -b nein -o worttabelle.csv -i ignor_liste.txt -l my-list.txt
```

## Voraussetzungen:

* python3
