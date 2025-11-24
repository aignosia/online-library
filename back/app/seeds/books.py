from pymarc import map_xml
from pymarc.record import Record

pg_fields = []


def list_field_tags(r: Record):
    for field in r.fields:
        if field.tag not in pg_fields:
            pg_fields.append(field.tag)


pg_series = []


def list_book_series(r: Record):
    for serie in r.series:
        pg_fields.append(serie.value())


def show(r: Record):
    print(
        list(map(lambda x: f"{x.tag}: {x.value()}", r.get_fields("245", "240")))
    )


author_subfields = []


def show_author_subfields(r: Record):
    author_field = r.get_fields("100")[0] if r.get_fields("100") else None

    if author_field:
        for subfield in author_field.subfields:
            if subfield.code not in author_subfields:
                author_subfields.append(subfield.code)


map_xml(show_author_subfields, "downloads/pgmarc.xml")

print(author_subfields)

# print(pg_fields)
# with open("downloads/field_series.txt", "w") as f:
#     f.write("; ".join(pg_fields))
