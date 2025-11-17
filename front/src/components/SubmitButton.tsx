interface LargeButtonProps {
  color: string;
  hoverColor: string;
  content: string;
}

export default function SubmitButton(props: LargeButtonProps) {
  return (
    <button
      type="submit"
      className={`bg-[${props.color}] hover:bg-[${props.hoverColor}] text-black font-medium py-2 rounded-md transition-colors`}
    >
      {props.content}
    </button>
  );
}
