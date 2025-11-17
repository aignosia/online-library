interface ButtonProps {
  color: string;
  hoverColor: string;
  content: string;
  onClick: CallableFunction;
}

export default function Button(props: ButtonProps) {
  return (
    <button
      className={`bg-[${props.color}] hover:bg-[${props.hoverColor}] font-medium text-gray-700 hover:text-gray-900 px-6 py-2 rounded-md transition-colors`}
      onClick={() => props.onClick()}
    >
      {props.content}
    </button>
  );
}
