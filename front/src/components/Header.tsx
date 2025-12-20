import { Link } from "react-router";
import Button from "./Button";
import { useNavigate } from "react-router";
import { useContext, useState } from "react";
import { AuthContext } from "../services/AuthContext";

export default function Header() {
  const auth = useContext(AuthContext);
  const navigate = useNavigate();

  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLoginButtonClick = () => {
    navigate("/login");
  };

  const handleUserButtonClick = () => {
    setIsMenuOpen((prev) => !prev);
  };
  return (
    <header className="w-full">
      <nav className="px-[3vw] h-17 py-4 w-full flex justify-between items-center bg-white">
        <div className="text-2xl text-gray-700 font-bold flex">
          {/*<img src={logo} alt="Logo" className="w-7" />*/}
          <Link to="/home">
            <p>
              <span className="text-[#f4b759]">Online</span>{" "}
              <span className="text-gray-700">Library</span>
            </p>
          </Link>
        </div>
        <div className="flex items-center gap-8">
          <div className="">
            <ul className="flex font-medium text-gray-900 gap-8">
              <li className="text-gray-700 hover:text-[#f4b759]">
                <Link to="/categories">Catégories</Link>
              </li>
              <li className="left-3.5 text-gray-700 hover:text-[#f4b759]">
                <Link to="/history">Historique</Link>
              </li>
            </ul>
          </div>
          <div className="text-gray-700">
            {auth.user ? (
              <>
                <button className="" onClick={handleUserButtonClick}>
                  {
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M18 20a6 6 0 0 0-12 0" />
                      <circle cx="12" cy="10" r="4" />
                      <circle cx="12" cy="12" r="10" />
                    </svg>
                  }
                </button>
                {isMenuOpen && (
                  <div className="absolute -ml-[130px] bg-white rounded-2xl p-3 shadow z-50 min-w-[150px]">
                    <p className="text-xl">{auth.user?.full_name || "User"}</p>
                    <p className="text-md text-gray-500">
                      {auth.user?.username}
                    </p>
                    <hr className="mt-2 mb-4 text-gray-300" />
                    <Button
                      color="#f4b759"
                      hoverColor="#f2a73e"
                      content="Déconnexion"
                      onClick={auth.logOut}
                    />
                  </div>
                )}
              </>
            ) : (
              <Button
                color="#f4b759"
                hoverColor="#f2a73e"
                content="Connexion"
                onClick={handleLoginButtonClick}
              />
            )}
          </div>
        </div>
      </nav>
    </header>
  );
}
