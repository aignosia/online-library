import BookList from "../components/BookList";
import Header from "../components/Header";
import { useContext, useEffect, useState } from "react";
import { apiClient } from "../services/api";
import { useSearchParams } from "react-router";
import { AuthContext } from "../services/AuthContext";
import { type Book } from "../App";

interface BookListingProps {
  title?: string;
  route?: string;
  authorization: boolean;
  hasPagination: boolean;
}

export default function BookListingPage(props: BookListingProps) {
  const auth = useContext(AuthContext);
  const [searchParams] = useSearchParams();
  const title = props.title || searchParams.get("name") || "";
  const route = props.route || searchParams.get("route") || "";

  const [books, setBooks] = useState<Book[]>([]);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(props.hasPagination);

  const fetchData = async (pageNumber: number) => {
    if (route) {
      const options = props.authorization
        ? {
            methods: "GET",
            headers: { Authorization: `Bearer ${auth.token}` },
          }
        : { methods: "GET" };
      let fetchingRoute = route;
      if (props.hasPagination) {
        fetchingRoute += fetchingRoute.includes("?") ? "&" : "?";
        fetchingRoute += `offset=${pageNumber}&limit=20`;
      }
      const data = await apiClient.request(fetchingRoute, options);
      setBooks((prev) => [...prev, ...data.books]);

      if (pageNumber >= data.max_offset) setHasMore(false);
    }
  };

  useEffect(() => {
    fetchData(0);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleLoadMore = () => {
    const nextPage = page + 1;
    setPage(nextPage);
    fetchData(nextPage);
  };

  return (
    <div className="h-screen flex flex-col bg-[#f8f5f1] overflow-y-hidden">
      <Header />
      <div className="flex flex-col flex-1 overflow-y-hidden">
        <BookList
          books={books}
          title={title}
          hasMorePage={hasMore}
          onLoadMore={handleLoadMore}
        />
      </div>
    </div>
  );
}
