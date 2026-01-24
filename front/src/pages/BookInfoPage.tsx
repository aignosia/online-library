import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { apiClient } from "../services/api";
import { type Book, type Author } from "../App";
import Header from "../components/Header";
import cover from "../assets/default-book-cover.png";
import DownloadButton from "../components/DownloadButton";
import BookCard from "../components/BookCard";

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
  const [similarBooks, setSimilarBooks] = useState<Array<Book>>([]);
  const [hasCover, setHasCover] = useState(true);
  useEffect(() => {
    const fetchData = async () => {
      const fetchedBook = await apiClient.request(`books/${id}`, {
        method: "GET",
      });
      setBook(fetchedBook);
      const similarBookNum = 60;
      const fetchedSimilarBooks = await apiClient.request(
        `books/${id}/recommendations?limit=${similarBookNum}`,
      );
      const start = Math.floor(Math.random() * (similarBookNum - 6));
      const end = start + 12;
      setSimilarBooks(fetchedSimilarBooks.slice(start, end));
    };
    fetchData();
  }, [id]);
  return (
    <div className="h-screen flex flex-col bg-[#f8f5f1] min-h-screen">
      <Header />
      <div className="w-full flex flex-col flex-1 px-[5vw] md:px-[10vw] lg:px-[20vw] py-12 overflow-y-auto">
        <div className="flex flex-col lg:flex-row w-full">
          <div className="lg:min-w-50 m-auto lg:m-0">
            <img
              src={hasCover ? book?.cover || cover : cover}
              alt="Book Cover"
              className="min-w-50 w-full max-w-60"
              onError={() => setHasCover(false)}
            />
          </div>
          <div className="mt-6 lg:mt-0 flex flex-col lg:pl-[5vw] gap-2 text-lg">
            <h1 className="font-bold text-xl lg:text-3xl text-center lg:text-left">
              {book?.title || "Title"}
            </h1>
            <p className="text-gray-600 text-xl text-center lg:text-left">
              {book?.authors
                .map((a) =>
                  `${a.firstname || ""} ${a.lastname || ""}`
                    .replace(",", "")
                    .trim(),
                )
                .join(", ") || "N/a"}
            </p>
            <p className="text-center lg:text-left">
              {[
                book?.publisher?.name.replace(",", "") || "",
                book?.pub_year,
              ].join(", ")}
            </p>
            <div className="pt-3 m-auto lg:m-0">
              <DownloadButton
                color="#f4b759"
                hoverColor="#f2a73e"
                options={book?.files}
              />
            </div>
            <div className="pt-10 flex flex-col gap-2 wrap-break-word">
              <span className="font-bold">Résumé :</span>
              <p className="whitespace-pre-wrap wrap-break-word">
                {book?.summary}
              </p>
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
                <ul className="list-disc list-inside lg:list-outside wrap-break-word">
                  {book?.notes.map((note, index) => (
                    <li key={index}>{note}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
        <div className="flex flex-col w-full py-10">
          <h1 className="font-bold text-2xl py-5">Livres similaires</h1>
          <div className="w-full grid grid-cols-[repeat(auto-fit,minmax(150px,1fr))] gap-5">
            {similarBooks.map((it) => {
              const authorsString = it.authors
                .map((a) =>
                  `${a.firstname ? a.firstname + " " : ""}${a.lastname}`
                    .replace(",", "")
                    .trim(),
                )
                .join(", ");
              return (
                <BookCard
                  key={`book${it.id}`}
                  id={it.id}
                  title={it.title}
                  author={authorsString}
                  cover={it.cover}
                />
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
