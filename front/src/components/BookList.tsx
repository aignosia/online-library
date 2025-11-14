import type { Book } from "../App";
import BookCard from "./BookCard";

interface BookListProps {
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
    <div className="pb-8 flex-1 overflow-y-auto scrollbar-hidden overflow-visible">
      <div className="pt-7 flex-1 grid grid-cols-[repeat(auto-fit,minmax(180px,1fr))] gap-10 overflow-visible">
        {items.map((it) => it)}
      </div>
    </div>
  );
}
