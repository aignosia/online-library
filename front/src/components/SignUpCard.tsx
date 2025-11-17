import SubmitButton from "./SubmitButton";
import TextInput from "./TextInput";
import { Link } from "react-router";

export default function SignUpCard() {
  return (
    <div className="bg-white shadow-xl rounded-3xl p-10 w-[450px]">
      <h2 className="text-2xl font-semibold text-center mb-10">
        Créer un compte
      </h2>

      <form className="flex flex-col">
        <TextInput placeholder="Enter Your Name" type="text" />
        <div className="h-6"></div>
        <TextInput placeholder="Enter Email" type="email" />
        <div className="h-6"></div>
        <TextInput placeholder="Enter Password" type="password" />
        <div className="h-6"></div>
        <TextInput placeholder="Confirm Password" type="password" />
        <div className="h-12"></div>

        <SubmitButton
          color="#f4b759"
          hoverColor="#f2a73e"
          content="Créer un compte"
        />
      </form>

      <div className="my-4 flex items-center justify-center gap-2 text-gray-400">
        <span className="h-px w-10 bg-gray-300"></span>
        <span className="text-sm">
          Vous avez déjà un compte?{" "}
          <Link to="/login">
            <u>Se connecter</u>
          </Link>
        </span>
        <span className="h-px w-10 bg-gray-300"></span>
      </div>
    </div>
  );
}
