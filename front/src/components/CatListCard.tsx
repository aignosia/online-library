import CatCard from "./CatCard";

interface CatListProps {
  categories: Array<string>;
}

export default function CatListCard(props: CatListProps) {
  return (
    <div className="h-full min-w-[200px] min-h-[50px] mt-7 py-6 px-6 mb-8 bg-[#f4b759] shadow-lg rounded-xl">
      <div className="h-full overflow-hidden overflow-y-auto scrollbar-hidden">
        <ul className="">
          {props.categories.map((it) => {
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
