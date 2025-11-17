import type { Book } from "../App";
import BookCard from "./BookCard";

interface BookListProps {
  title: string;
  books: Array<Book>;
}
export default function BookList(props: BookListProps) {
  const bookCards = props.books.map((it) => {
    return <BookCard key="book1" title={it.title} author={it.author} />;
  });

  const minCols = 5;
  const placeholdersNeeded = Math.max(0, minCols - bookCards.length);
  const placeholders = [];

  for (let i = 0; i < placeholdersNeeded; i++)
    placeholders.push(<div key={"ph" + i}></div>);

  const items = [...bookCards, ...placeholders];
  return (
    <div className="flex flex-col flex-1 pb-8 px-8 overflow-y-auto scrollbar-hidden">
      <div className="bg-[#f8f5f1] py-8">
        <h1 className="text-3xl font-bold">{props.title}</h1>
      </div>
      <div className="pt-7 flex-1 grid grid-cols-[repeat(auto-fit,minmax(180px,1fr))] gap-10">
        {items.map((it) => it)}
      </div>
    </div>
  );
}
