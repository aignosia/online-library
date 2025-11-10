export default function Header() {
  return (
    <header className="w-full">
      <nav className="px-10 py-6 w-full flex justify-between items-center bg-[#f8f5f1]">
        {/* #2C52CE */}
        <div className="text-2xl text-gray-900 font-bold flex space-x-3">
          {/*<img src={logo} alt="Logo" className="w-7" />*/}
          <p>Online Library</p>
        </div>
        <div className="flex space-x-8">
          <ul className="flex space-x-8 font-medium text-gray-900">
            {/*<li>
              <a href="/">Recommandations</a>
            </li>*/}
            <li>
              <a href="/">Catégories</a>
            </li>
            <li className="left-3.5">
              <a href="/">Historique</a>
            </li>
          </ul>
          <div>
            <a href="/">
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
            </a>
          </div>
        </div>
      </nav>
    </header>
  );
}
