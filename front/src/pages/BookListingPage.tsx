import type { Book } from "../App";
import BookList from "../components/BookList";
import Header from "../components/Header";

interface BookListingProps {
  title: string;
  books: Array<Book>;
}
export default function BookListingPage(props: BookListingProps) {
  return (
    <div className="h-screen flex flex-col bg-[#f8f5f1] overflow-y-hidden">
      <Header />
      <div className="flex flex-col flex-1 px-[20vw] overflow-y-hidden">
        <BookList books={props.books} title={props.title} />
      </div>
    </div>
  );
}
