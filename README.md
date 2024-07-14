# Codecentric Repo Crawler

## Nutzen des Tools

Der Repo Crawler erlaubt eine Datenbasis die einfach dazu genutzt werden kann Personen zu finden, die Expertise in einer bestimmten Programmiersprache haben und bei Codecentric arbeiten. Genutzt wird dazu die GitHub API.

## Installation

Das Tool beruht auf Python. Am einfachsten ist es ein Python Environment mit Conda aufzusetzen. Da zum Suchen keien Dependencies gebraucht werden, kann auch ein existierendes Environment benutzt werden.

```bash
conda create -n env_name python=3.12.3
conda activate env_name
```

Die Datenbank ist vorbefüllt und die Suchfunktion kann so schon genutzt werden. Falls die Datenbasis neu gefüllt werden soll, müssen folgende Abhängigkeiten mit pip installiert werden.

```bash
pip install python-dotenv
pip install requests
```

## Nutzung

Zum Suchen nach Personen die Erfahrung mit einer Programmiersprache haben kann folgender Befehl ausgeführt werden:

```bash
python read_db.py
```

Dort werden dann alle verfügbaren Sprachen dargestellt. Nach der Aufforderung nach der Eingabe einer Sprache wird diese geprüft und entsprechende Ergebnisse dargestellt.

### Befüllen der Datenbank

Falls die Datenbank aktualisiert werden soll, muss ein GitHub Token erstellt werden mit folgenden Rechten:

- public_repo
- read:org
- read:project
- read:user

Anschließend muss eine .env Datei im Projektordner angelegt werden mit folgendem Inhalt

```env
GITHUB_TOKEN=YOUR_TOKEN
```

Dann kann die Datenbank mit einem Befehl initiiert, befüllt oder auch nur neue Werte ergänzt werden. Alte bleiben dabei bestehen.

```bash
python fill_db.py
```

## Hintergründe

Das Tool basiert auf Python, das sich gut für solch kurze Skripte eignet. In Hintergrund steht eine sehr leichtgewichtige SQLite Datenbank.

Das Befüllen der Datenbank läuft über zwei Wege. Zum ersten werden die persönlichen Repos alle Codecentric Mitglieder gecrawlt und in der Datenbank gespeichert. Anschließend iteriert das Tool noch durch alle Codecentrric Repositories und ergänzt alle, bei denen codecentric Mitglieder contributed haben.
