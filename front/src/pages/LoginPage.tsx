import { useNavigate } from "react-router";
import Button from "../components/Button";
import LoginCard from "../components/LoginCard";
import SignUpCard from "../components/SignUpCard";

interface LoginPageProps {
  type: "signup" | "login";
}

export default function LoginPage(props: LoginPageProps) {
  const navigate = useNavigate();
  function navigateToSignUp() {
    navigate("/signup");
  }
  function navigateToLogin() {
    navigate("/login");
  }
  return (
    <div className="min-h-screen bg-[#f8f5f1] flex flex-col">
      <header className="w-full h-17 flex justify-between items-center px-[3vw] py-4">
        <h1 className="text-2xl font-bold text-gray-900">
          <span className="text-[#f4b759]">Online</span>{" "}
          <span className="text-gray-700">Library</span>
        </h1>
        <div className="flex items-center gap-6">
          <Button
            color="#f4b759"
            hoverColor="#f2a73e"
            content={props.type == "login" ? "Créer un compte" : "Connexion"}
            onClick={props.type == "login" ? navigateToSignUp : navigateToLogin}
          />
        </div>
      </header>

      <main className="grow flex justify-center items-center px-4">
        <div className="relative flex flex-col md:flex-row items-center -mt-[104px]">
          {props.type == "signup" ? <SignUpCard /> : <LoginCard />}
        </div>
      </main>
    </div>
  );
}
