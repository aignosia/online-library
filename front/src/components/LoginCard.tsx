import { Link } from "react-router";
import SubmitButton from "./SubmitButton";
import TextInput from "./TextInput";
import { useContext, useState } from "react";
import { AuthContext } from "../services/AuthProvider";

export default function LoginCard() {
  const [input, setInput] = useState({
    username: "",
    password: "",
    grant_type: "password",
    scope: "",
    client_id: "",
    client_secret: "",
  });

  const auth = useContext(AuthContext);

  const handleSubmitEvent = (e) => {
    e.preventDefault();
    if (input.username !== "" && input.password !== "") {
      auth.loginAction(new URLSearchParams(input));
      return;
    }
    alert("Saisissez des informations valides");
  };
  const handleInput = (e) => {
    const { name, value } = e.target;
    setInput((prev) => ({
      ...prev,
      [name]: value,
    }));
  };
  return (
    <div className="bg-white shadow-xl rounded-3xl p-10 w-[450px]">
      <h2 className="text-2xl font-semibold text-center mb-10">Connexion</h2>

      <form className="flex flex-col" onSubmit={handleSubmitEvent}>
        <TextInput
          placeholder="Enter Username"
          type="text"
          name="username"
          onChange={handleInput}
        />
        <div className="h-10"></div>
        <TextInput
          placeholder="Enter Password"
          name="password"
          type="password"
          onChange={handleInput}
        />

        <p className="text-sm text-gray-500 mt-2 mb-12">
          <Link to="/">
            <u>Mot de passe oubliée?</u>
          </Link>
        </p>

        <SubmitButton
          color="#f4b759"
          hoverColor="#f2a73e"
          content="Connexion"
        />
      </form>

      <div className="my-4 flex items-center justify-center gap-2 text-gray-400">
        <span className="h-px w-10 bg-gray-300"></span>
        <span className="text-sm">
          <Link to="/signup">
            <u>Créer un compte</u>
          </Link>
        </span>
        <span className="h-px w-10 bg-gray-300"></span>
      </div>
    </div>
  );
}
