import { Link } from "react-router";
import SubmitButton from "./SubmitButton";
import TextInput from "./TextInput";
import { useContext, useState, type ChangeEvent, type FormEvent } from "react";
import { AuthContext } from "../services/AuthContext";

export default function LoginCard() {
  const [input, setInput] = useState({
    username: "",
    password: "",
    grant_type: "password",
    scope: "",
    client_id: "",
    client_secret: "",
  });
  const [authError, setAuthError] = useState(false);

  const auth = useContext(AuthContext);

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (input.username !== "" && input.password !== "") {
      auth.loginAction(new URLSearchParams(input));
      if (!auth.user) setAuthError(true);
      return;
    }
    setAuthError(true);
  };

  const handleInput = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setInput((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <div className="flex flex-col bg-white shadow-xl rounded-3xl p-10 w-[450px]">
      <h2 className="text-2xl font-semibold text-center mb-10">Connexion</h2>

      <form className="flex flex-col" onSubmit={handleSubmit}>
        <TextInput
          placeholder="Enter Username"
          type="text"
          name="username"
          autoComplete="username"
          onChange={handleInput}
        />
        <div className="h-10"></div>
        <TextInput
          placeholder="Enter Password"
          name="password"
          type="password"
          autoComplete="current-password"
          onChange={handleInput}
        />

        <p className="text-sm text-gray-500 mt-2 mb-12">
          <Link to="/">
            <u>Mot de passe oubliée?</u>
          </Link>
        </p>

        {authError && (
          <p className="text-red-500 -mt-5 mb-5">
            Saisissez des informations valides.
          </p>
        )}

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
