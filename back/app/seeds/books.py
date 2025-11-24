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


map_xml(show, "downloads/pgmarc.xml")

# print(pg_fields)
# with open("downloads/field_series.txt", "w") as f:
#     f.write("; ".join(pg_fields))
