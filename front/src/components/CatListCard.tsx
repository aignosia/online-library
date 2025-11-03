import { CatCard } from "./CatCard";

export function CatListCard() {
  const categories = [
    "Litérature",
    "Science et technologie",
    "Histoire",
    "Sciences sociales et société",
    "Art et culture",
    "Religion et philosophie",
    "Santé et médecine",
    "Éducation et références",
    "Mode de vie et loisirs",
  ];
  return (
    <div className="h-full min-w-[300px] min-h-[50px] mt-7 py-10 px-10 mb-8 bg-white shadow-lg rounded-lg">
      <div className="h-full overflow-hidden overflow-y-auto scrollbar-hidden">
        <ul className="divide-y divide-gray-200">
          {categories.map((it) => {
            return (
              <li>
                <a href="/">
                  <CatCard content={it} />
                </a>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}
