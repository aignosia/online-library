import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import json

    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    return json, mo, pd, plt, sns


@app.cell
def _(json, pd):
    df = pd.read_csv("data/pg_books.csv")
    df["authors"] = df["authors"].apply(json.loads)
    df["subjects"] = df["subjects"].apply(json.loads)
    df["classes"] = df["classes"].apply(json.loads)
    df["subclasses"] = df["subclasses"].apply(json.loads)
    df["language_code"] = df["language_code"].apply(lambda x: x[:2])
    return (df,)


@app.cell
def _(df):
    lc_stat = df["language_code"].describe()

    df_authors = df.copy()
    df_authors["authors"] = df_authors["authors"].apply(lambda x: [e.get("name") for e in x])
    df_authors = df_authors.explode("authors")
    authors_stat = df_authors["authors"].describe()

    df_subjects = df.explode("subjects")
    subjects_stat = df_subjects["subjects"].describe()

    df_classes = df.explode("classes")
    classes_stat = df_classes["classes"].describe()

    df_subclasses = df.explode("subclasses")
    sc_stat = df_subclasses["subclasses"].describe()
    return (
        authors_stat,
        classes_stat,
        df_classes,
        df_subclasses,
        df_subjects,
        lc_stat,
        sc_stat,
        subjects_stat,
    )


@app.cell
def _(authors_stat, classes_stat, lc_stat, pd, sc_stat, subjects_stat):
    stats = pd.DataFrame({
        "": ["count", "unique", "top", "freq"],
        "language_code": [lc_stat["count"], lc_stat["unique"], lc_stat["top"], lc_stat["freq"]],
        "authors": [authors_stat["count"], authors_stat["unique"], authors_stat["top"], authors_stat["freq"]],
        "subjects": [subjects_stat["count"], subjects_stat["unique"], subjects_stat["top"], subjects_stat["freq"]],
        "classes": [classes_stat["count"], classes_stat["unique"], classes_stat["top"], classes_stat["freq"]],
        "subclasses": [sc_stat["count"], sc_stat["unique"], sc_stat["top"], sc_stat["freq"]],
    })
    stats
    return


@app.cell
def _(df, pd, plt, sns):
    df["pub_year"] = (
        pd.to_numeric(df["pub_year"], errors="coerce")
        .fillna(0)
        .astype(int)
        .astype(str)
    )

    plt.figure(figsize=(20, 8))
    ax1 = sns.countplot(
        data=df.sort_values("pub_year"), x="pub_year", color="teal"
    )

    # 4. Esthétique
    plt.title("Nombre de livres par année (comptage catégoriel)", fontsize=16)
    plt.xticks(
        rotation=90
    )  # Rotation verticale pour que chaque année soit lisible
    plt.xlabel("Année")
    plt.ylabel("Nombre de livres")
    plt.grid(axis="y", alpha=0.3)
    ax1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2004 est l'année où le plus de livre a été créé avec environ 7000 livres créés cette année. 2005 est le suivant avec un peu moins de 5000 livres. Les autres années ont tous moins de 4000 livres.
    """)
    return


@app.cell
def _(df, plt, sns):
    df["language_code"] = df["language_code"].str.split(" ").str[0]
    lang_counts = df["language_code"].value_counts()

    # Création du graphique
    plt.figure(figsize=(12, 6))
    ax2 = sns.barplot(x=lang_counts.index, y=lang_counts.values)

    # Personnalisation
    plt.title("Distribution des livres par code de langue", fontsize=15)
    plt.xlabel("Code de langue", fontsize=12)
    plt.ylabel("Nombre de livres", fontsize=12)
    plt.xticks(rotation=90)  # Rotation pour éviter que les codes se chevauchent
    ax2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    L'anglais est la langue la plus présente dans les livres avec 60000 livres qui sont en anglais. L'anglais domine très largement les autres langues ayant moins de 5000 livres chacun.
    """)
    return


@app.cell
def _(df_subjects, plt, sns):
    top_subjects = df_subjects["subjects"].value_counts().head(20)

    plt.figure(figsize=(12, 8))
    ax3 = sns.barplot(
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
    ax3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La méthode TF-IDF peut ne pas avoir beaucoup de sens vu que la plupart des livres sont des livres de science-fiction et d'histoires courtes. Solution : TF-IDF sur les métadonnées.
    """)
    return


@app.cell
def _(df_classes, plt, sns):
    top_classes = df_classes["classes"].value_counts()

    plt.figure(figsize=(12, 8))
    ax4 = sns.barplot(
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
    ax4
    return


@app.cell
def _(df_subclasses, plt, sns):
    top_subclasses = df_subclasses["subclasses"].value_counts().head(20)

    plt.figure(figsize=(12, 8))
    ax5 = sns.barplot(
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
    ax5
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Les statistiques des classes et des sous-classes sont normales. Comme ce sont les livres de fiction qui dominent, il est naturel que ce soit la classe Language and literature qui est la plus prépondérante et que ce soient des sous-classes qui appartiennent à cette classe qui ont le plus de livre (American literature, English literature, etc).
    """)
    return


if __name__ == "__main__":
    app.run()
