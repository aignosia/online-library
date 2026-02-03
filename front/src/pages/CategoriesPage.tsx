import { Link } from "react-router";
import type { Categorie } from "../App";
import Header from "../components/Header";
import { useEffect, useState } from "react";
import { apiClient } from "../services/api";

export default function CategoriesPage() {
  const [categories, setCategories] = useState<Categorie[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const fetchedCategories = await apiClient.request("classes", {
        method: "GET",
      });
      fetchedCategories.sort((a: Categorie, b: Categorie) =>
        a.name.localeCompare(b.name),
      );
      setCategories(fetchedCategories);
    };
    fetchData();
  }, []);
  return (
    <div className="h-screen flex flex-col bg-[#f8f5f1] overflow-y-hidden">
      <Header />
      <div className="flex flex-col px-[5vw] md:px-[20vw] py-8 overflow-y-auto">
        <h1 className="text-3xl pb-5">Categories</h1>
        <div className="columns-1 md:columns-2 lg:columns-3 md:gap-8">
          {categories
            .sort((a, b) => a.name.localeCompare(b.name))
            .map((cat) => {
              return (
                <div
                  key={cat.id}
                  className="py-2 font-medium text-lg text-gray-900 break-inside-avoid"
                >
                  <p className="pb-2 font-semibold text-xl">{cat.name}</p>
                  {cat.subclasses
                    .sort((a, b) => a.name.localeCompare(b.name))
                    .map((sc, index) => {
                      return (
                        <Link
                          key={index}
                          to={{
                            pathname: `/category/${sc.id}`,
                            search: `?name=${encodeURIComponent(sc.name)}&route=${encodeURIComponent(`subclasses/${sc.id}/books?offset=0&limit=50`)}`,
                          }}
                        >
                          <p className="hover:text-gray-500">{sc.name}</p>
                        </Link>
                      );
                    })}
                </div>
              );
            })}
        </div>
      </div>
    </div>
  );
}
