import sqlite3

# Connect to database
con = sqlite3.connect("codecentric_repo.db")
cur = con.cursor()

print("Welcome to the codecentric repository search tool")
print(
    "This tool allows you to search for codecentric members who contributed to repositories in a specific language."
)
print(
    "------------------------------------------------------------------------------------------------------------"
)

# Print all available languages
found_languages = cur.execute(
    """
    SELECT DISTINCT language
    FROM repo
    """
).fetchall()

available_languages = ""
languages_list = []

print("Available languages are:")
for index, row in enumerate(found_languages):
    if row[0] is not None:
        if len(available_languages + row[0]) > 80:
            print(available_languages[:-2])
            available_languages = ""
        available_languages = available_languages + row[0] + ", "
        languages_list.append(row[0])


print(available_languages[:-2])
print(
    "------------------------------------------------------------------------------------------------------------"
)

# read input from console
language = ""
while language not in languages_list:
    language = input("Please enter a language to search for: ")
    if language not in languages_list:
        print("Language not found. Please try again.")
print(
    "------------------------------------------------------------------------------------------------------------"
)

# Search database
result = cur.execute(
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
).fetchall()

persons = []
repos = []

# Catch no results found
if len(result) == 0:
    print("No results found")
    con.close()
    exit()

# Print results by person
print(
    f"Found the following persons that contributed to repositories, that mainly use {language}:"
)
for row in result:
    if row[0] is None or row[1] is None:
        continue
    if row[0] not in persons:
        persons.append(row[0])
        repos.append(row[1])
    else:
        repos[len(persons) - 1] = repos[len(persons) - 1] + ", " + row[1]

for i in range(len(persons)):
    print(f"{persons[i]} contributed in the following repositories: {repos[i]}")

con.close()
