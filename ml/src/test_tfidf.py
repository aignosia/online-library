import pickle

import pandas as pd

df = pd.read_csv("data/pg_books.csv")
df = pd.DataFrame(df.iloc[:1000])

with open("models/tfidf_matrix.pkl", "rb") as f:
    cosine_sim = pickle.load(f)


def get_recommandations(book: pd.DataFrame, cosine_sim=cosine_sim):
    id = book.index
    sim_scores = list(enumerate(cosine_sim[id][0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]

    book_indices = [i[0] for i in sim_scores]

    return df[["authors", "title"]].iloc[book_indices]


if __name__ == "__main__":
    i = 195
    print("Book:", df.iloc[[i]][["authors", "title"]])
    recommendations = get_recommandations(df.iloc[[i]])
    print("Recommendations:\n", recommendations)
