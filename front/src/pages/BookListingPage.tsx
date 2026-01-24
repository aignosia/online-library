import BookList from "../components/BookList";
import Header from "../components/Header";
import { useContext, useEffect, useState } from "react";
import { apiClient } from "../services/api";
import { useSearchParams } from "react-router";
import { AuthContext } from "../services/AuthContext";

interface BookListingProps {
  title?: string;
  route?: string;
  authorization: boolean;
}

export default function BookListingPage(props: BookListingProps) {
  const auth = useContext(AuthContext);
  const [searchParams] = useSearchParams();
  const title = props.title || searchParams.get("name") || "";
  const route = props.route || searchParams.get("route");

  const [books, setBooks] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      if (route) {
        const options = props.authorization
          ? {
              methods: "GET",
              headers: { Authorization: `Bearer ${auth.token}` },
            }
          : { methods: "GET" };
        const data = await apiClient.request(route, options);
        setBooks(data);
      }
    };
    fetchData();
  }, [auth.token, props.authorization, route]);

  return (
    <div className="h-screen flex flex-col bg-[#f8f5f1] overflow-y-hidden">
      <Header />
      <div className="flex flex-col flex-1 overflow-y-hidden">
        <BookList books={books} title={title} />
      </div>
    </div>
  );
}
