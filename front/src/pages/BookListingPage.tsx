import BookList from "../components/BookList";
import Header from "../components/Header";
import { useEffect, useState } from "react";
import { apiClient } from "../services/api";
import { useSearchParams } from "react-router";

interface BookListingProps {
  title?: string;
  route?: string;
}

export default function BookListingPage(props: BookListingProps) {
  const [searchParams] = useSearchParams();
  const title = props.title || searchParams.get("name") || "";
  const route = props.route || searchParams.get("route");

  const [books, setBooks] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      if (route) {
        const data = await apiClient.request(route, {
          method: "GET",
        });
        setBooks(data);
      }
    };
    fetchData();
  }, [route]);

  return (
    <div className="h-screen flex flex-col bg-[#f8f5f1] overflow-y-hidden">
      <Header />
      <div className="flex flex-col flex-1 overflow-y-hidden">
        <BookList books={books} title={title} />
      </div>
    </div>
  );
}
