interface ButtonProps {
  color: string;
  hoverColor: string;
  content: any;
  onClick: CallableFunction;
}

export default function Button(props: ButtonProps) {
  return (
    <button
      style={
        {
          "--btn-color": props.color,
          "--btn-hover-color": props.hoverColor,
        } as React.CSSProperties
      }
      className="bg-(--btn-color) hover:bg-(--btn-hover-color) font-medium text-gray-700 hover:text-gray-900 px-6 py-2 rounded-md transition-colors"
      onClick={() => props.onClick()}
    >
      {props.content}
    </button>
  );
}
