interface LargeButtonProps {
  color: string;
  hoverColor: string;
  content: string;
}

export default function SubmitButton(props: LargeButtonProps) {
  return (
    <button
      type="submit"
      style={
        {
          "--btn-color": props.color,
          "--btn-hover-color": props.hoverColor,
        } as React.CSSProperties
      }
      className={`bg-(--btn-color) hover:bg-(--btn-hover-color) text-black font-medium py-2 rounded-md transition-colors`}
    >
      {props.content}
    </button>
  );
}
