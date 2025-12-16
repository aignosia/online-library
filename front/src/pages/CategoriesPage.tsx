import { Link } from "react-router";
import type { Categorie } from "../App";
import Header from "../components/Header";

interface CategoryPageProps {
  categories: Array<Categorie>;
}

export default function CategoriesPage(props: CategoryPageProps) {
  return (
    <div className=" bg-[#f8f5f1]">
      <Header />
      <div className="flex flex-col px-[20vw] py-8">
        <h1 className="text-3xl font-bold pb-5">Catégories</h1>
        <div className="columns-3 gap-8">
          {props.categories.map((cat) => {
            return (
              <div
                key={cat.id}
                className="px-6 py-2 font-medium text-lg text-gray-900 break-inside-avoid"
              >
                <p className="pb-2 font-bold text-xl">{cat.name}</p>
                {cat.subclasses.map((sc) => (
                  <Link
                    to={`/category/${sc.id}?name=${sc.name}&route=${"subclasses"}`}
                  >
                    <p className="hover:text-gray-500">{sc.name}</p>
                  </Link>
                ))}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
