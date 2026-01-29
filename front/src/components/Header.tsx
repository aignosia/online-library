import { Link } from "react-router";
import Button from "./Button";
import { useNavigate } from "react-router";
import { useContext, useState } from "react";
import { AuthContext } from "../services/AuthContext";
import logo from "/logo.png";
import { FaRegCircleUser } from "react-icons/fa6";
import { MdClose, MdMenu, MdSearch } from "react-icons/md";
import SearchBar from "./SearchBar";
import useHandleOutsideClick from "../hooks/useHandleOutsideClick";

export default function Header() {
  const auth = useContext(AuthContext);
  const navigate = useNavigate();
  const userMenuRef = useHandleOutsideClick(() => setIsMenuOpen(false));

  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isMobileNavOpen, setIsMobileNavOpen] = useState(false);
  const [isSearchBarOpen, setIsSearchBarOpen] = useState(false);
  const searchRef = useHandleOutsideClick(() => setIsSearchBarOpen(false));

  const handleLoginButtonClick = () => {
    navigate("/login");
  };

  const handleUserButtonClick = () => {
    setIsMenuOpen((prev) => !prev);
  };

  return (
    <header className="w-full">
      <nav className="px-[5vw] md:px-[3vw] h-17 py-4 w-full flex justify-between items-center bg-white">
        <Link to="/home">
          <div className="text-2xl text-gray-700 font-bold flex gap-2">
            {/* Logo and title */}
            <img src={logo} alt="Logo" className="h-7 -translate-y-0.5" />
            <p className="text-[#f4b759]">RecoMind</p>
          </div>
        </Link>
        <div className="hidden md:flex w-[50%] bg-white z-30">
          <SearchBar />
        </div>
        {/* Desktop navigation menu*/}
        <div className="hidden lg:flex items-center gap-8">
          <div className="">
            <ul className="flex font-medium gap-8">
              <li className="text-gray-700 hover:text-[#f4b759]">
                <Link to="/categories">Categories</Link>
              </li>
              {auth.user ? (
                <li className="text-gray-700 hover:text-[#f4b759]">
                  <Link to="/history">History</Link>
                </li>
              ) : (
                <></>
              )}
            </ul>
          </div>
          <div className="text-gray-700">
            {auth.user ? (
              <>
                <button
                  className="hover:text-[#f2a73e] translate-y-1"
                  onClick={handleUserButtonClick}
                >
                  <FaRegCircleUser className="w-5 h-5" />
                </button>
                {isMenuOpen && (
                  <div
                    ref={userMenuRef}
                    className="absolute -ml-[130px] bg-white rounded-2xl p-3 shadow z-50 min-w-[150px]"
                  >
                    <p className="text-xl">{auth.user?.full_name || "User"}</p>
                    <p className="text-md text-gray-500">{auth.user?.email}</p>
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
                content="Sign in"
                onClick={handleLoginButtonClick}
              />
            )}
          </div>
        </div>
        {/* Mobile components */}
        {isSearchBarOpen ? (
          <div
            ref={searchRef}
            className="lg:hidden absolute w-[75%] bg-white z-30"
          >
            <SearchBar autoFocus={true} />
          </div>
        ) : (
          <></>
        )}
        <div className="lg:hidden w-fit flex items-center gap-4">
          {isSearchBarOpen ? (
            <></>
          ) : (
            <button
              className="flex md:hidden"
              onClick={() => setIsSearchBarOpen(true)}
            >
              <MdSearch className="w-7 h-7" />
            </button>
          )}
          <button
            className="lg:hidden p-2 text-gray-700 z-40"
            onClick={() => setIsMobileNavOpen((prev) => !prev)}
          >
            {isMobileNavOpen ? (
              <MdClose className="w-7 h-7" />
            ) : (
              <MdMenu className="w-7 h-7" />
            )}
          </button>
        </div>

        {/* Mobile menu overlay */}
        {isMobileNavOpen && (
          <div className="fixed inset-0 bg-white z-30 flex flex-col p-8 pt-24 gap-6 lg:hidden animate-in slide-in-from-top duration-300">
            <ul className="flex flex-col font-medium text-xl text-gray-900 gap-6">
              <li>
                <Link
                  to="/categories"
                  onClick={() => setIsMobileNavOpen(false)}
                >
                  Categories
                </Link>
              </li>
              {auth.user ? (
                <li>
                  <Link to="/history" onClick={() => setIsMobileNavOpen(false)}>
                    History
                  </Link>
                </li>
              ) : (
                <></>
              )}
            </ul>

            <div className="mt-4 border-t pt-6">
              {auth.user ? (
                <div className="space-y-4">
                  <p className="text-xl font-medium">{auth.user?.full_name}</p>
                  <Button
                    color="#f4b759"
                    hoverColor="#f2a73e"
                    content="Log out"
                    onClick={() => {
                      auth.logOut();
                      setIsMobileNavOpen(false);
                    }}
                  />
                </div>
              ) : (
                <Button
                  color="#f4b759"
                  hoverColor="#f2a73e"
                  content="Sign in"
                  onClick={handleLoginButtonClick}
                />
              )}
            </div>
          </div>
        )}
      </nav>
    </header>
  );
}
