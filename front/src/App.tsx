import "./App.css";
import { Header } from "./components/Header";
import { BookCard } from "./components/BookCard";
import { SearchBar } from "./components/SearchBar";
import { CatListCard } from "./components/CatListCard";

function App() {
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
    <>
      <div className="h-screen flex flex-col bg-[#F8F9FD]">
        <Header />
        <div className="flex-1 flex flex-col pt-6 overflow-hidden">
          <div className="">
            <SearchBar />
          </div>
          <div className="mt-6 flex flex-1 overflow-hidden">
            <div className="flex-1 flex flex-col">
              <div className="px-8">
                <p className="text-gray-400 pb-2 text-lg">Recommandations</p>
                <div className="w-full h-px mx-auto border border-[#C7C6CB]"></div>
              </div>
              <div className="px-8 pb-8 flex-1 overflow-y-auto scrollbar-hidden overflow-visible">
                <div className="pt-7 flex-1 grid grid-cols-[repeat(auto-fit,minmax(180px,1fr))] gap-10 overflow-visible">
                  {items.map((it) => it)}
                </div>
              </div>
            </div>
            <div className="w-1/3 pr-8 flex flex-col">
              <p className="text-gray-400 pb-2 text-lg">
                Principales catégories
              </p>
              <div className="w-full h-px border border-[#C7C6CB]"></div>
              <CatListCard />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
