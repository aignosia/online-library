interface CatCardProps {
  content: string;
}

export default function CatCard(props: CatCardProps) {
  return (
    <div className="px-5 py-4 hover:bg-[#f4b759] rounded-xl text-lg font-medium text-gray-700 hover:text-gray-900">
      {props.content}
    </div>
  );
}
