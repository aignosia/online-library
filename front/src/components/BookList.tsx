import type { Book } from "../App";
import BookCard from "./BookCard";

interface BookListProps {
  title: string;
  books: Array<Book>;
}
export default function BookList(props: BookListProps) {
  const bookCards = props.books.map((it) => {
    const authorsString = it.authors
      .map((a) =>
        `${a.firstname ? a.firstname + " " : ""}${a.lastname || ""}`
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
  });

  return (
    <div className="flex flex-col flex-1 lg:pb-8 px-[5vw] md:px-[10vw] lg:px-[20vw] overflow-y-auto py-4">
      <div className="bg-[#f8f5f1] pb-4 lg:py-8">
        <p className="text-gray-600 text-2xl lg:text-3xl font-semibold">
          {props.title}
        </p>
      </div>
      <div className="lg:pt-7 flex-1 grid grid-cols-[repeat(auto-fit,minmax(150px,1fr))] lg:grid-cols-[repeat(auto-fit,minmax(170px,1fr))] gap-5 md:gap-10">
        {bookCards.map((it) => it)}
      </div>
    </div>
  );
}
