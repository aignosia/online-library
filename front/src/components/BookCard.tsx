import { Link } from "react-router";
import cover from "../assets/default-book-cover.png";

interface BookCardProps {
  id: number;
  title: string;
  author: string;
  cover: string | null;
}

export default function BookCard(props: BookCardProps) {
  return (
    <Link to={`/book/${props.id}`}>
      <div className="mr-0 min-w-10 md:flex-1 rounded-xl bg-white overflow-hidden shadow-lg hover:scale-105">
        <img
          src={props.cover || cover}
          alt="Book Cover"
          className="w-full object-cover"
        />
        <div className="p-4">
          <p className="text-lg text-gray-500 h-12 overflow-clip">
            {props.title}
          </p>
          <p className="mt-4 text-lg">{props.author}</p>
        </div>
      </div>
    </Link>
  );
}
