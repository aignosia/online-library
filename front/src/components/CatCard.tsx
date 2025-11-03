export function CatCard(props) {
  return (
    <div className="p-5 hover:bg-gray-100">
      <p className="text-xl">{props.content}</p>
    </div>
  );
}
