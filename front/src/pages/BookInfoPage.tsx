import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { apiClient } from "../services/api";
import type { Author } from "../App";
import Header from "../components/Header";
import cover from "../assets/book-cover.jpg";
import Button from "../components/Button";

interface Publisher {
  id: number;
  name: string;
}

interface Serie {
  id: number;
  name: string;
}

interface Subject {
  id: number;
  name: string;
}

interface BookClass {
  id: number;
  name: string;
}

interface Subclass {
  id: number;
  name: string;
  bookclass: BookClass | null;
}

interface BookFull {
  title: string;
  pub_year: number;
  summary: string;
  isbn: string | null;
  notes: string | null;
  language_code: string | null;
  cover: string | null;
  publisher: Publisher | null;
  serie: Serie | null;
  authors: Array<Author>;
  subjects: Array<Subject>;
  files: Array<object>;
  subclasses: Array<Subclass>;
}

export default function BookInfoPage() {
  const { id } = useParams();
  const [book, setBook] = useState<BookFull>();
  useEffect(() => {
    const fetchData = async () => {
      const data = await apiClient.request(`books/${id}`, {
        method: "GET",
      });
      setBook(data);
    };
    fetchData();
  }, [id]);
  return (
    <div className="bg-[#f8f5f1] min-h-screen">
      <Header />
      <div className="px-[20vw] py-12">
        <div className="flex">
          <div className="min-w-50">
            <img src={book?.cover || cover} alt="Book Cover" />
          </div>
          <div className="flex flex-col pl-15 gap-2 text-lg">
            <h1 className="font-bold text-3xl">{book?.title || "Title"}</h1>
            <p className="text-gray-600 text-xl">
              {book?.authors
                .map((a) =>
                  `${a.firstname || ""} ${a.lastname || ""}`
                    .replace(",", "")
                    .trim(),
                )
                .join(", ") || "N/a"}
            </p>
            <p>
              {[
                book?.publisher?.name.replace(",", "") || "",
                book?.pub_year,
              ].join(", ")}
            </p>
            <div className="pt-3">
              <Button
                color="#f4b759"
                hoverColor="#f2a73e"
                content="Télécharger"
                onClick={() => {}}
              />
            </div>
            <p className="pt-10">
              <span className="font-bold">Résumé :</span> {book?.summary}
            </p>
            {book?.serie ? <p>Serie: {book?.serie?.name}</p> : <></>}
            <p>
              <span className="font-bold">Catégorie(s) :</span>{" "}
              {book?.subclasses.map((sc) => sc.name).join(", ") || "N/a"}
            </p>
            <p>
              <span className="font-bold">ISBN :</span> {book?.isbn || "N/a"}
            </p>
            <p>
              <span className="font-bold">Langue :</span>{" "}
              {book?.language_code || "N/a"}
            </p>
            <p>
              <span className="font-bold">Mots clés :</span>{" "}
              {book?.subjects.map((s) => s.name).join(", ") || "N/a"}
            </p>
            {book?.notes && (
              <p>
                <span className="font-bold">Notes :</span> {book?.notes}
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
