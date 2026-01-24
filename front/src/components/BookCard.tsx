import { useState } from "react";
import { Link } from "react-router";
import cover from "../assets/default-book-cover.png";

interface BookCardProps {
  id: number;
  title: string;
  author: string;
  cover: string | null;
}

export default function BookCard(props: BookCardProps) {
  const [hasCover, setHasCover] = useState(true);
  return (
    <Link to={`/book/${props.id}`}>
      <div className="m-auto min-w-20 basis-1/5 max-w-50 h-full flex flex-col rounded-xl bg-white overflow-hidden shadow-lg hover:scale-105">
        <div className="flex items- flex-1">
          <img
            src={hasCover ? props.cover || cover : cover}
            alt="Book Cover"
            className="w-full object-cover max-h-80"
            onError={() => setHasCover(false)}
          />
        </div>
        <div className="p-4">
          <p className="text-lg h-13 overflow-clip">{props.title}</p>
          <p className="mt-4 text-gray-500 text-lg overflow-clip h-13">
            {props.author}
          </p>
        </div>
      </div>
    </Link>
  );
}
