import { Link } from "react-router";
import cover from "../assets/default-book-cover.png";
import { useState } from "react";

interface BookCardProps {
  id: number;
  title: string;
  author: string;
  cover: string;
}

export default function BookCard(props: BookCardProps) {
  const [hasError, setHasError] = useState(false);
  return (
    <Link to={`/book/${props.id}`}>
      <div className="m-auto min-w-12 basis-1/5 max-w-50 h-full flex flex-col rounded-xl bg-white overflow-hidden shadow-lg hover:scale-105">
        <div className="flex flex-1 h-full w-full min-h-70 overflow-hidden">
          <img
            src={hasError ? cover : props.cover}
            alt="Book Cover"
            className="w-full h-full object-cover"
            loading="lazy"
            onError={() => setHasError(true)}
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
