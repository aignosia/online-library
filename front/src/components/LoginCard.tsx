import { Link } from "react-router";
import SubmitButton from "./SubmitButton";
import TextInput from "./TextInput";
import { useContext, useState, type ChangeEvent, type FormEvent } from "react";
import { AuthContext } from "../services/AuthContext";
import { FaEyeSlash } from "react-icons/fa6";
import { FaEye } from "react-icons/fa";

export default function LoginCard() {
  const [input, setInput] = useState({
    username: "",
    password: "",
    grant_type: "password",
    scope: "",
    client_id: "",
    client_secret: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [authError, setAuthError] = useState(false);

  const auth = useContext(AuthContext);

  const toggleVisibility = () => {
    setShowPassword((prev) => !prev);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setAuthError(false);
    if (input.username !== "" && input.password !== "") {
      try {
        await auth.loginAction(new URLSearchParams(input));
      } catch (err) {
        console.log(err);
        setAuthError(true);
      }
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
      <h2 className="text-2xl font-semibold text-center mb-10">Login</h2>

      <form className="flex flex-col" onSubmit={handleSubmit}>
        <TextInput
          placeholder="Enter Username"
          type="text"
          name="username"
          autoComplete="username"
          onChange={handleInput}
        />
        <div className="h-10"></div>
        <div className="flex items-center">
          <TextInput
            placeholder="Enter Password"
            name="password"
            type={showPassword ? "text" : "password"}
            autoComplete="current-password"
            onChange={handleInput}
          />
          <button
            type="button"
            onClick={toggleVisibility}
            className="absolute right-14 flex items-center text-gray-400 hover:text-gray-600 focus:outline-none"
            title={
              showPassword
                ? "Masquer le mot de passe"
                : "Afficher le mot de passe"
            }
          >
            {showPassword ? (
              <FaEyeSlash size={20} className="transition-opacity" />
            ) : (
              <FaEye size={20} className="transition-opacity" />
            )}
          </button>
        </div>

        <p className="text-sm text-gray-500 mt-2 mb-12">
          <Link to="/">
            <u>Don't remember password?</u>
          </Link>
        </p>

        {authError && (
          <p className="text-red-500 -mt-5 mb-5">Enter valid informations.</p>
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
            <u>Sign up</u>
          </Link>
        </span>
        <span className="h-px w-10 bg-gray-300"></span>
      </div>
    </div>
  );
}
