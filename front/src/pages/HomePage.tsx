import { useContext, useEffect, useState } from "react";
import type { Book, Categorie } from "../App";
import BookCard from "../components/BookCard";
import CatListCard from "../components/CatListCard";
import Header from "../components/Header";
import { AuthContext } from "../services/AuthContext";
import { apiClient } from "../services/api";
import { LoadingPage } from "./LoadingPage";

export default function HomePage() {
  const auth = useContext(AuthContext);
  const [books, setBooks] = useState<Book[]>([]);
  const [categories, setCategories] = useState<Categorie[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      const limit = 20;
      let endpoint = "";
      if (auth.user) {
        endpoint = `users/me/books/recommendations?limit=${limit}`;
        setBooks(
          await apiClient.request(endpoint, {
            method: "GET",
            headers: {
              Authorization: `Bearer ${auth.token}`,
            },
          }),
        );
      } else {
        endpoint = `books/popular?limit=${limit}`;
        const data = await apiClient.request(endpoint, {
          method: "GET",
        });
        setBooks(data.books);
      }
      const fetchedCategories = await apiClient.request("classes", {
        method: "GET",
      });
      fetchedCategories.sort((a: Categorie, b: Categorie) =>
        a.name.localeCompare(b.name),
      );
      setCategories(fetchedCategories);
      setIsLoading(false);
    };

    fetchData();
  }, [auth.token, auth.user]);

  return (
    <>
      {isLoading ? (
        <LoadingPage />
      ) : (
        <div className="h-screen flex flex-col bg-[#f8f5f1] overflow-hidden">
          <Header />
          <div className="flex-1 flex flex-col md:px-[3vw] lg:-ml-8 overflow-hidden">
            <div className="flex flex-1 overflow-y-auto lg:overflow-hidden pt-6">
              <div className="flex-1 flex flex-col">
                <div className="px-4 md:px-8">
                  <p className="text-gray-600 pb-2 font-semibold text-2xl">
                    {auth.user ? "Recommended" : "Popular"}
                  </p>
                  <div className="hidden lg:flex w-full h-px mx-auto border border-gray-400"></div>
                </div>
                <div className="pb-8 px-4 md:px-8 flex-1 lg:overflow-y-auto scrollbar-hidden">
                  <div className="pt-7 grid grid-cols-[repeat(auto-fit,minmax(144px,1fr))] md:grid-cols-[repeat(auto-fit,minmax(170px,1fr))] gap-6 md:gap-10">
                    {books.map((it) => {
                      const authorsString = it.authors
                        .map((a) =>
                          `${a.firstname ? a.firstname + " " : ""}${a.lastname ?? ""}`.replace(
                            ",",
                            "",
                          ),
                        )
                        .join(", ");
                      return (
                        <BookCard
                          key={`book${it.id}`}
                          id={it.id}
                          title={it.title}
                          author={authorsString}
                          cover={it.cover || ""}
                        />
                      );
                    })}
                  </div>
                </div>
              </div>
              <div className="hidden w-[500px] lg:flex flex-col">
                <p className="text-gray-600 pb-2 font-semibold text-2xl">
                  Main Categories
                </p>
                <div className="w-full h-px border border-gray-400"></div>
                <CatListCard categories={categories} />
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
