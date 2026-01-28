import { Link, useNavigate } from "react-router";
import Button from "../components/Button";
import LoginCard from "../components/LoginCard";
import SignUpCard from "../components/SignUpCard";
import logo from "/logo.png";

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
    <div className="min-h-screen bg-[#f8f5f1] flex flex-col pb-4 overflow-hidden">
      <header className="w-full h-17 flex justify-between items-center px-[5vw] md:px-[3vw] py-4">
        <Link to="/home">
          <div className="flex gap-2">
            <img src={logo} alt="Logo" className="h-7" />
            <h1 className="text-2xl font-bold text-gray-900">
              <span className="text-[#f4b759]">RecoMind</span>
            </h1>
          </div>
        </Link>
        <div className="flex items-center">
          <Button
            color="#f4b759"
            hoverColor="#f2a73e"
            content={props.type == "login" ? "Sign up" : "Sign in"}
            onClick={props.type == "login" ? navigateToSignUp : navigateToLogin}
          />
        </div>
      </header>

      <main className="grow flex justify-center items-center px-4">
        <div className="relative flex flex-col md:flex-row items-center lg:-mt-[104px] py-4">
          {props.type == "signup" ? <SignUpCard /> : <LoginCard />}
        </div>
      </main>
    </div>
  );
}
