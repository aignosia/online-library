import { Link } from "react-router";
import type { Categorie } from "../App";
import CatCard from "./CatCard";

interface CatListProps {
  categories: Array<Categorie>;
}

export default function CatListCard(props: CatListProps) {
  return (
    <div className="hidden md:flex min-h-[50px] mt-7 py-6 px-4 mb-8 bg-white shadow-lg rounded-xl">
      <div className="h-full overflow-hidden overflow-y-auto">
        <ul className="">
          {props.categories.map((cat) => {
            return (
              <li key={`cat${cat.id}`}>
                <Link
                  to={{
                    pathname: `/main-category/${cat.id}`,
                    search: `?name=${encodeURIComponent(cat.name)}&route=${encodeURIComponent(`classes/${cat.id}/books`)}`,
                  }}
                >
                  <CatCard content={cat.name} />
                </Link>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}
