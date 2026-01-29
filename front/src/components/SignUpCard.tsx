import { useContext, useState, type ChangeEvent, type FormEvent } from "react";
import SubmitButton from "./SubmitButton";
import TextInput from "./TextInput";
import { Link } from "react-router";
import { AuthContext } from "../services/AuthContext";
import { FaEye, FaEyeSlash } from "react-icons/fa";

export default function SignUpCard() {
  const [input, setInput] = useState({
    username: "",
    full_name: "",
    is_active: true,
    password: "",
  });
  const [authData, setAuthData] = useState({
    username: "",
    password: "",
    grant_type: "password",
    scope: "",
    client_id: "",
    client_secret: "",
  });

  const [errors, setErrors] = useState({
    auth: false,
    password: false,
    confirm: false,
  });

  const [showPassword, setShowPassword] = useState(false);

  const toggleVisibility = () => {
    setShowPassword((prev) => !prev);
  };

  const auth = useContext(AuthContext);

  const handleInput = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (name !== "confirm")
      setInput((prev) => ({
        ...prev,
        [name]: value,
      }));

    if (name == "password" && value.length < 8) {
      setErrors((prev) => ({ ...prev, password: true }));
    } else if (name == "password") {
      setErrors((prev) => ({ ...prev, password: false }));
    }

    if (name == "confirm" && value !== input.password) {
      setErrors((prev) => ({ ...prev, confirm: true }));
    } else if (name == "confirm") {
      setErrors((prev) => ({ ...prev, confirm: false }));
    }
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (
      input.username !== "" &&
      input.full_name !== "" &&
      input.password !== "" &&
      input.password.length >= 8
    ) {
      const signupAction = async () => {
        setAuthData((prev) => ({
          ...prev,
          username: input.username,
          password: input.password,
        }));
        const response = await fetch(`${import.meta.env.VITE_API_URL}/users`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(input),
        });
        if (response.ok) {
          auth.loginAction(new URLSearchParams(authData));
        } else if (response.status == 422) {
          setErrors((prev) => ({ ...prev, auth: true }));
        }
      };
      signupAction();
      return;
    }
    setErrors((prev) => ({ ...prev, auth: true }));
  };

  return (
    <div className="bg-white shadow-xl rounded-3xl p-10 w-[450px]">
      <h2 className="text-2xl font-semibold text-center mb-10">Sign up</h2>

      <form className="flex flex-col" onSubmit={handleSubmit}>
        <TextInput
          placeholder="Enter your name"
          type="text"
          name="full_name"
          autoComplete="name"
          onChange={handleInput}
        />
        <div className="h-6"></div>
        <TextInput
          placeholder="Enter email"
          type="email"
          name="username"
          autoComplete="username"
          onChange={handleInput}
        />
        <div className="h-6"></div>
        <div className="flex items-center">
          <TextInput
            placeholder="Enter Password"
            name="password"
            type={showPassword ? "text" : "password"}
            autoComplete="new-password"
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
        <div className="h-6"></div>
        {errors.password && (
          <p className="text-red-500 -mt-3 mb-3">
            Le mot de passe doit contenir au moins 8 caractères.
          </p>
        )}
        <div className="flex items-center">
          <TextInput
            placeholder="Confirm Password"
            name="confirm"
            type={showPassword ? "text" : "password"}
            autoComplete="new-password"
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
        {errors.confirm && (
          <p className="text-red-500 mt-3">
            Les mots de passe ne correspondent pas.
          </p>
        )}
        <div className="h-12"></div>

        {errors.auth && (
          <p className="text-red-500 -mt-5 mb-5">
            Saisissez des informations valides.
          </p>
        )}

        <SubmitButton color="#f4b759" hoverColor="#f2a73e" content="Sign up" />
      </form>

      <div className="my-4 flex items-center justify-center gap-2 text-gray-400">
        <span className="h-px w-10 bg-gray-300"></span>
        <span className="text-sm">
          Already have an account?{" "}
          <Link to="/login">
            <u>Sign in</u>
          </Link>
        </span>
        <span className="h-px w-10 bg-gray-300"></span>
      </div>
    </div>
  );
}
