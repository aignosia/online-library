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
    <div className="h-screen flex flex-col bg-[#f8f5f1]">
      <Header />
      <div className="flex-1 flex flex-col pt-6 px-[3vw] -ml-8 overflow-hidden">
        <div className="">
          <SearchBar />
        </div>
        <div className="mt-6 flex flex-1 overflow-hidden">
          <div className="flex-1 flex flex-col">
            <div className="px-8">
              <p className="text-gray-600 pb-2 text-lg">Recommandations</p>
              <div className="w-full h-px mx-auto border border-gray-400"></div>
            </div>
            <div className="pb-8 px-8 flex-1 overflow-y-auto scrollbar-hidden overflow-visible">
              <div className="pt-7 flex-1 grid grid-cols-[repeat(auto-fit,minmax(180px,1fr))] gap-10 overflow-visible">
                {items.map((it) => it)}
              </div>
            </div>
          </div>
          <div className="w-[500px] flex flex-col">
            <p className="text-gray-500 pb-2 text-lg">Principales catégories</p>
            <div className="w-full h-px border border-gray-400"></div>
            <CatListCard categories={props.categories} />
          </div>
        </div>
      </div>
    </div>
  );
}
