import sqlite3

con = sqlite3.connect("codecentric_repo.db")
cur = con.cursor()

# read input from console
language = input("Enter a language: ")

cursor = cur.execute(
    """
    SELECT real_name, repo.full_name
    FROM person_repo
    JOIN person ON person_repo.login = person.login
    JOIN repo ON person_repo.full_name = repo.full_name
    WHERE language = '{}'
    ORDER BY real_name
    """.format(
        language
    )
)

perons = []
repos = []

for row in cursor.fetchall():
    if row[0] not in perons:
        perons.append(row[0])
        repos.append(row[1])
    else:
        repos[len(perons) - 1] = repos[len(perons) - 1] + ", " + row[1]

for i in range(len(perons)):
    print(
        f"{perons[i]} contributed in the following repositories, that mainly use {language}: {repos[i]}"
    )

con.close()