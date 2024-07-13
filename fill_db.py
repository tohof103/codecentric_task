import requests
import sqlite3
import os
from dotenv import load_dotenv

con = sqlite3.connect("codecentric_repo.db")
cur = con.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS person(
        login TEXT PRIMARY KEY,
        real_name TEXT
    )
    """
)
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS repo(
        full_name TEXT PRIMARY KEY,
        language TEXT
    )
    """
)
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS person_repo(
        login TEXT,
        full_name TEXT,
        FOREIGN KEY(login) REFERENCES person(login),
        FOREIGN KEY(full_name) REFERENCES repo(full_name)
    )
    """
)

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

headers = {"Authorization": f"token {token}"}

members = requests.get(
    "https://api.github.com/orgs/codecentric/members", headers=headers
).json()

for person in members:
    name = requests.get(
        f"https://api.github.com/users/{person['login']}", headers=headers
    ).json()["name"]
    user_repos = requests.get(
        f"https://api.github.com/users/{person['login']}/repos", headers=headers
    ).json()
    print(f"Add person to db: {person['login']}, {name}")
    cur.execute("INSERT OR IGNORE INTO person VALUES (?, ?)", (person["login"], name))
    for r in user_repos:
        repo_name = r["full_name"]
        language = r["language"]
        print(f"Add repo to db: {repo_name}, {language}")
        cur.execute("INSERT OR IGNORE INTO repo VALUES (?, ?)", (repo_name, language))
        print(f"Add person-repo to db: {person['login']}, {repo_name}")
        cur.execute(
            "INSERT OR IGNORE INTO person_repo VALUES (?, ?)",
            (person["login"], repo_name),
        )

con.commit()
con.close()
