export function SearchBar() {
  return (
    <div className="w-full max-w-2xl mx-auto flex">
      <span className="transform translate-y-1/5 translate-x-8 text-[#C7C6CB]">
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
          <path d="m21 21-4.34-4.34" />
          <circle cx="11" cy="11" r="8" />
        </svg>
      </span>
      <input
        type="text"
        placeholder="Rechercher..."
        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-gray-400 "
      />
    </div>
  );
}
