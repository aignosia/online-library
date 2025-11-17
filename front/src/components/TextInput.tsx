interface TextInputProps {
  placeholder: string;
  type: string;
  name: string;
  onChange(e: React.ChangeEventHandler<HTMLInputElement>): void;
}
export default function TextInput(props: TextInputProps) {
  const handleOnChange = (e) => {
    props.onChange(e);
  };
  return (
    <input
      type={props.type}
      placeholder={props.placeholder}
      name={props.name}
      onChange={handleOnChange}
      className="w-full border border-gray-200 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-yellow-400"
    />
  );
}
