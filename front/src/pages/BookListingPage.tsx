import { useParams } from "react-router";
import BookList from "../components/BookList";
import Header from "../components/Header";
import { useEffect, useState } from "react";
import { apiClient } from "../services/api";
import { useSearchParams } from "react-router";

interface BookListingProps {
  title: string;
  route?: string;
}

export default function BookListingPage(props: BookListingProps) {
  const params = useParams();
  const id = params.id;
  const [searchParams] = useSearchParams();
  const name = searchParams.get("name") || "";
  const route = searchParams.get("route");

  const [books, setBooks] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = await apiClient.request(
        props.route || `${route}/${id}` || "books",
        {
          method: "GET",
        },
      );
      setBooks(data.books || data);
    };
    fetchData();
  }, [id, props.route, route]);

  return (
    <div className="h-screen flex flex-col bg-[#f8f5f1] overflow-y-hidden">
      <Header />
      <div className="flex flex-col flex-1 px-[20vw] overflow-y-hidden">
        <BookList books={books} title={props.title || name} />
      </div>
    </div>
  );
}
