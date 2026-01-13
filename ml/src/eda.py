# %%
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import chi2_contingency

# %%
df = pd.read_csv("../data/pg_books.csv")
df["authors"] = df["authors"].apply(json.loads)
df["subjects"] = df["subjects"].apply(json.loads)
df["classes"] = df["classes"].apply(json.loads)
df["subclasses"] = df["subclasses"].apply(json.loads)
df["language_code"] = df["language_code"].apply(lambda x: x[:2])
df.head()

# %%
lc_stat = df["language_code"].describe()

df_authors = df.copy()
df_authors["authors"] = df_authors["authors"].apply(
    lambda x: [e.get("name") for e in x]
)
df_authors = df_authors.explode("authors")
authors_stat = df_authors["authors"].describe()

df_subjects = df.explode("subjects")
subjects_stat = df_subjects["subjects"].describe()

df_classes = df.explode("classes")
classes_stat = df_classes["classes"].describe()

df_subclasses = df.explode("subclasses")
sc_stat = df_subclasses["subclasses"].describe()

# %%
stats = pd.DataFrame(
    {
        "": ["count", "unique", "top", "freq"],
        "language_code": [
            lc_stat["count"],
            lc_stat["unique"],
            lc_stat["top"],
            lc_stat["freq"],
        ],
        "authors": [
            authors_stat["count"],
            authors_stat["unique"],
            authors_stat["top"],
            authors_stat["freq"],
        ],
        "subjects": [
            subjects_stat["count"],
            subjects_stat["unique"],
            subjects_stat["top"],
            subjects_stat["freq"],
        ],
        "classes": [
            classes_stat["count"],
            classes_stat["unique"],
            classes_stat["top"],
            classes_stat["freq"],
        ],
        "subclasses": [
            sc_stat["count"],
            sc_stat["unique"],
            sc_stat["top"],
            sc_stat["freq"],
        ],
    }
)
stats

# %%
df["pub_year"] = (
    pd.to_numeric(df["pub_year"], errors="coerce")
    .fillna(0)
    .astype(int)
    .astype(str)
)

plt.figure(figsize=(12, 6))
sns.countplot(data=df.sort_values("pub_year"), x="pub_year", color="teal")

plt.title("Nombre de livres par année (comptage catégoriel)", fontsize=16)
plt.xticks(rotation=90)
plt.xlabel("Année")
plt.ylabel("Nombre de livres")
plt.grid(axis="y", alpha=0.3)
plt.show()

# %% [markdown]
"""
2004 was the year in which the most books were created, with around 7,000 books
created that year. 2005 was next, with just under 5,000 books. All other years
had fewer than 4,000 books.
"""

# %%
df["language_code"] = df["language_code"].str.split(" ").str[0]
lang_counts = df["language_code"].value_counts()

plt.figure(figsize=(12, 6))
sns.barplot(x=lang_counts.index, y=lang_counts.values)

plt.title("Distribution des livres par code de langue", fontsize=15)
plt.xlabel("Code de langue", fontsize=12)
plt.ylabel("Nombre de livres", fontsize=12)
plt.xticks(rotation=90)
plt.show()

# %% [markdown]
"""
English is the most common language in books, with 60,000 books written in English.
English largely dominates other languages, with fewer than 5,000 books written in
each of the other languages.
"""

# %%
top_subjects = df_subjects["subjects"].value_counts().head(20)

plt.figure(figsize=(12, 8))
sns.barplot(
    x=top_subjects.values,
    y=top_subjects.index,
    hue=top_subjects.index,
    palette="viridis",
    legend=False,
)

plt.title("Top 20 des sujets les plus fréquents", fontsize=15)
plt.xlabel("Nombre d'occurrences", fontsize=12)
plt.ylabel("Sujets", fontsize=12)
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()

# %% [markdown]
"""
The TF-IDF method may not be very useful, given that most of the books are science
fiction and short stories. Solution: TF-IDF on metadata.
"""

# %%
top_classes = df_classes["classes"].value_counts()

sns.barplot(
    x=top_classes.values,
    y=top_classes.index,
    hue=top_classes.index,
    palette="viridis",
    legend=False,
)

plt.title("Classement des classes", fontsize=15)
plt.xlabel("Nombre d'occurrences", fontsize=12)
plt.ylabel("Classes", fontsize=12)
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()

# %%
top_subclasses = df_subclasses["subclasses"].value_counts().head(20)

plt.figure(figsize=(12, 8))
sns.barplot(
    x=top_subclasses.values,
    y=top_subclasses.index,
    hue=top_subclasses.index,
    palette="viridis",
    legend=False,
)

plt.title("Classement des sous-classes", fontsize=15)
plt.xlabel("Nombre d'occurrences", fontsize=12)
plt.ylabel("Sous-classes", fontsize=12)
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()

# %% [markdown]
"""
The statistics for the classes and subclasses are normal a priori. Since
fiction books dominate, it is natural that the Language and literature class
is the most prevalent and that the subclasses belonging to this class have the
most books (American literature, English literature, etc.).
"""


# %%
def cramers_v(x, y):
    contingency_table = pd.crosstab(x, y)
    chi2_statistic, p_value, dof, expected = chi2_contingency(contingency_table)

    n = contingency_table.sum().sum()
    phi2 = chi2_statistic / n
    r, k = contingency_table.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    k_corr = k - (k - 1) * (k - 2) / (n - 1)
    r_corr = r - (r - 1) * (r - 2) / (n - 1)
    v = np.sqrt(phi2corr / min(k_corr - 1, r_corr - 1))

    return v


cols = ["subjects", "classes"]
df_corr = df[cols].explode("subjects")
df_corr = df_corr.explode("classes").dropna().head(10000)

corr_matrix = pd.DataFrame(index=cols, columns=cols)  # ty:ignore[invalid-argument-type]

for col1 in cols:
    for col2 in cols:
        corr_matrix.loc[col1, col2] = cramers_v(df_corr[col1], df_corr[col2])

corr_matrix = corr_matrix.astype(float)

print(corr_matrix)

sns.heatmap(corr_matrix, annot=True, cmap="Blues", vmin=0, vmax=1)
plt.title("Matrice d'association (V de Cramer)")
plt.show()

# %% [markdown]
"""
The dataset needed to be truncated because the number of book is too large and
is not supported by the python kernel for computations needed to calculate the
Cramer's V. It appears though that there is significant correlation (> 0.5)
between the subjects and the classes of the book (and thus between the subjects
and the subclasses). The correlation is good for TF-IDF but might lead to
over-weighting. If the recommendations lack diversity, avoiding using subclasses
might be good.
"""
