import { Link } from "react-router";
import type { Categorie } from "../App";
import Header from "../components/Header";

interface CategoryPageProps {
  categories: Array<Categorie>;
}

export default function CategoriesPage(props: CategoryPageProps) {
  return (
    <div className="h-screen flex flex-col bg-[#f8f5f1] overflow-y-hidden">
      <Header />
      <div className="flex flex-col px-[5vw] md:px-[20vw] py-8 overflow-y-auto">
        <h1 className="text-3xl font-bold pb-5">Catégories</h1>
        <div className="columns-1 md:columns-2 lg:columns-3 md:gap-8">
          {props.categories
            .sort((a, b) => a.name.localeCompare(b.name))
            .map((cat) => {
              return (
                <div
                  key={cat.id}
                  className="py-2 font-medium text-lg text-gray-900 break-inside-avoid"
                >
                  <p className="pb-2 font-bold text-xl">{cat.name}</p>
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
