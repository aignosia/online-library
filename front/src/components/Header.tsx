import { Link } from "react-router";

export default function Header() {
  return (
    <header className="w-full">
      <nav className="px-[3vw] py-6 w-full flex justify-between items-center bg-white">
        {/* #2C52CE */}
        <div className="text-2xl text-gray-700 font-bold flex space-x-3">
          {/*<img src={logo} alt="Logo" className="w-7" />*/}
          <Link to="/home">
            <p>
              <span className="text-[#f4b759]">Online</span>{" "}
              <span className="text-gray-700">Library</span>
            </p>
          </Link>
        </div>
        <div className="flex space-x-8">
          <ul className="flex space-x-8 font-medium text-gray-900">
            {/*<li>
              <a href="/">Recommandations</a>
            </li>*/}
            <li className="text-gray-700 hover:text-gray-900">
              <Link to="/categories">Catégories</Link>
            </li>
            <li className="left-3.5 text-gray-700 hover:text-gray-900">
              <Link to="/history">Historique</Link>
            </li>
          </ul>
          <div className="text-gray-700 hover:text-gray-900">
            <Link to="/login">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M18 20a6 6 0 0 0-12 0" />
                <circle cx="12" cy="10" r="4" />
                <circle cx="12" cy="12" r="10" />
              </svg>
            </Link>
          </div>
        </div>
      </nav>
    </header>
  );
}
