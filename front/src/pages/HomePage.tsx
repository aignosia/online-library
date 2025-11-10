import BookCard from "../components/BookCard";
import CatListCard from "../components/CatListCard";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";

export default function HomePage() {
  const books = [
    <BookCard
      key="book1"
      title="An Inquiry into the Nature and Causes of the Wealth of Nations"
      author="Adam Smith"
    />,
    <BookCard
      key="book1"
      title="An Inquiry into the Nature and Causes of the Wealth of Nations"
      author="Adam Smith"
    />,
    <BookCard
      key="book1"
      title="An Inquiry into the Nature and Causes of the Wealth of Nations"
      author="Adam Smith"
    />,
    <BookCard
      key="book1"
      title="An Inquiry into the Nature and Causes of the Wealth of Nations"
      author="Adam Smith"
    />,
    <BookCard
      key="book1"
      title="An Inquiry into the Nature and Causes of the Wealth of Nations"
      author="Adam Smith"
    />,
  ];

  const minCols = 7;
  const placeholdersNeeded = Math.max(0, minCols - books.length);
  const placeholders = [];

  for (let i = 0; i < placeholdersNeeded; i++)
    placeholders.push(<div key={"ph" + i}></div>);

  const items = [...books, ...placeholders];
  return (
    <div className="h-screen flex flex-col bg-[#f8f5f1]">
      <Header />
      <div className="flex-1 flex flex-col pt-6 overflow-hidden">
        <div className="">
          <SearchBar />
        </div>
        <div className="mt-6 flex flex-1 overflow-hidden">
          <div className="flex-1 flex flex-col">
            <div className="px-8">
              <p className="text-gray-500 pb-2 text-lg">Recommandations</p>
              <div className="w-full h-px mx-auto border border-gray-400"></div>
            </div>
            <div className="px-8 pb-8 flex-1 overflow-y-auto scrollbar-hidden overflow-visible">
              <div className="pt-7 flex-1 grid grid-cols-[repeat(auto-fit,minmax(180px,1fr))] gap-10 overflow-visible">
                {items.map((it) => it)}
              </div>
            </div>
          </div>
          <div className="w-1/3 pr-8 flex flex-col">
            <p className="text-gray-500 pb-2 text-lg">Principales catégories</p>
            <div className="w-full h-px border border-gray-400"></div>
            <CatListCard />
          </div>
        </div>
      </div>
    </div>
  );
}
