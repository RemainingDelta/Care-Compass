import pandas as pd

CREATE TABLE health_articles (
    id INT PRIMARY KEY,
    country VARCHAR(100),
    article_title VARCHAR(255),
    article_link TEXT,
    source VARCHAR(100)
);

# Load your CSV
df = pd.read_csv("datasets/raw-datasets/Healthcare Articles.csv")

# Open the output SQL file
with open("database-files/article_inserts.sql", "w", encoding='utf-8') as f:
    f.write("INSERT INTO health_articles (id, country, article_title, article_link, source) VALUES\n")

    values = []
    for _, row in df.iterrows():
        id_ = int(row['id'])
        country = row['country'].replace("'", "''")
        title = row['article_title'].replace("'", "''")
        link = row['article_link'].replace("'", "''")
        source = row['source'].replace("'", "''")

        values.append(f"({id_}, '{country}', '{title}', '{link}', '{source}')")

    f.write(",\n".join(values) + ";\n")