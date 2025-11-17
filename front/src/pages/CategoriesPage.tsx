import Header from "../components/Header";

interface CategoryPageProps {
  categories: Array<string>;
}

export default function CategoriesPage(props: CategoryPageProps) {
  const subcat = ["Économie", "Philosophie", "Mathématiques", "Physiques"];
  return (
    <div className="h-screen bg-[#f8f5f1]">
      <Header />
      <div className="flex px-[20vw] py-8">
        <div className="w-1/3 px-6 py-6 bg-[#f4b759] rounded-xl shadow-lg">
          {props.categories.map((it) => {
            return (
              <div className="px-6 py-4 hover:bg-[#f2a73e] rounded-lg font-medium text-lg text-gray-700 hover:text-gray-900">
                {it}
              </div>
            );
          })}
        </div>
        <div className="ml-5 p-8 bg-white grow h-fit space-y-5 rounded-xl shadow-lg">
          {subcat.map((it) => {
            return (
              <div className="p-4 bg-[#f8f5f1] hover:bg-[#e1dbc9] rounded-lg text-lg text-gray-700 hover:text-gray-900">
                {it}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
