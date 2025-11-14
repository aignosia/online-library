interface CatCardProps {
  content: string;
}
export default function CatCard(props: CatCardProps) {
  return (
    <div className="p-5 hover:bg-[#f2a73e] rounded-xl text-lg text-gray-700 hover:text-gray-900">
      {props.content}
    </div>
  );
}
