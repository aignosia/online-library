import type { Book, Categorie } from "../App";
import BookCard from "../components/BookCard";
import CatListCard from "../components/CatListCard";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";

interface HomePageProps {
  categories: Array<Categorie>;
  books: Array<Book>;
}

export default function HomePage(props: HomePageProps) {
  const bookCards = props.books.map((it) => {
    const authorsString = it.authors
      .map((a) => `${a.firstname ?? ""} ${a.lastname ?? ""}`.replace(",", ""))
      .join(", ");
    return (
      <BookCard
        key={`book${it.id}`}
        id={it.id}
        title={it.title}
        author={authorsString}
        cover={it.cover}
      />
    );
  });

  const minCols = 5;
  const placeholdersNeeded = Math.max(0, minCols - bookCards.length);
  const placeholders = [];

  for (let i = 0; i < placeholdersNeeded; i++)
    placeholders.push(<div key={"ph" + i}></div>);

  const items = [...bookCards, ...placeholders];
  return (
    <div className="h-screen flex flex-col bg-[#f8f5f1] overflow-hidden">
      <Header />
      <div className="flex-1 flex flex-col lg:pt-6 md:px-[3vw] lg:-ml-8 overflow-hidden">
        <div className="hidden lg:flex">
          <SearchBar />
        </div>
        <div className="flex flex-1 overflow-y-auto lg:overflow-hidden pt-6">
          <div className="flex-1 flex flex-col">
            <div className="px-8">
              <p className="text-gray-600 pb-2 font-semibold text-2xl">
                Recommandations
              </p>
              <div className="hidden lg:flex w-full h-px mx-auto border border-gray-400"></div>
            </div>
            <div className="pb-8 px-8 flex-1 lg:overflow-y-auto scrollbar-hidden">
              <div className="pt-7 flex-1 grid grid-cols-[repeat(auto-fit,minmax(150px,1fr))] lg:grid-cols-[repeat(auto-fit,minmax(170px,1fr))] gap-3 md:gap-10">
                {items.map((it) => it)}
              </div>
            </div>
          </div>
          <div className="hidden w-[500px] lg:flex flex-col">
            <p className="text-gray-600 pb-2 font-semibold text-2xl">
              Principales catégories
            </p>
            <div className="w-full h-px border border-gray-400"></div>
            <CatListCard categories={props.categories} />
          </div>
        </div>
      </div>
    </div>
  );
}
