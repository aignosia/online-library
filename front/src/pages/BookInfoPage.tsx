import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { apiClient } from "../services/api";
import type { Author } from "../App";
import Header from "../components/Header";
import cover from "../assets/book-cover.jpg";
import DownloadButton from "../components/DownloadButton";

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

export interface BookFile {
  id: number;
  label: string;
  type: string;
  book_id: string;
  location: string;
}

interface BookFull {
  title: string;
  pub_year: number;
  summary: string;
  isbn: string | null;
  notes: Array<string> | null;
  language_code: string | null;
  cover: string | null;
  publisher: Publisher | null;
  serie: Serie | null;
  authors: Array<Author>;
  subjects: Array<Subject>;
  files: Array<BookFile>;
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
              <DownloadButton
                color="#f4b759"
                hoverColor="#f2a73e"
                options={book?.files}
              />
            </div>
            <div className="pt-10 flex flex-col gap-2">
              <span className="font-bold">Résumé :</span>
              <p className="whitespace-pre-wrap">{book?.summary}</p>
            </div>
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
              <div className="flex flex-col gap-2">
                <span className="font-bold">Notes :</span>
                <ul className="list-disc list-outside">
                  {book?.notes.map((note, index) => (
                    <li key={index}>{note}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
