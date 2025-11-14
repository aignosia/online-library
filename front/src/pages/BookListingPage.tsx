import type { Book } from "../App";
import BookList from "../components/BookList";
import Header from "../components/Header";

interface BookListingProps {
  title: string;
  books: Array<Book>;
}
export default function BookListingPage(props: BookListingProps) {
  return (
    <div className="h-screen flex flex-col bg-[#f8f5f1] overflow-hidden">
      <Header />
      <div className="flex flex-col flex-1 px-[20vw] overflow-hidden">
        <div className="bg-[#f8f5f1] py-8">
          <h1 className="text-3xl font-bold">{props.title}</h1>
        </div>
        <BookList books={props.books} />
      </div>
    </div>
  );
}
