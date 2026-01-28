import { useEffect, useState } from "react";
import { apiClient } from "../services/api";
import { useNavigate } from "react-router";
import useHandleOutsideClick from "../hooks/useHandleOutsideClick";

export default function SearchBar() {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const suggestionsRef = useHandleOutsideClick(() => setShowSuggestions(false));

  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      const data = await apiClient.request(`books/autocomplete?q=${query}`, {
        method: "GET",
      });
      setSuggestions(data);
      setShowSuggestions(true);
    };
    const timer = setTimeout(() => {
      if (query.length > 2) {
        fetchData();
      } else {
        setSuggestions([]);
      }
    }, 300);
    return () => clearTimeout(timer);
  }, [query]);

  const handleSearchAction = (value: string) => {
    navigate(
      `/search?name=${encodeURIComponent(`Search: ${value}`)}&route=${encodeURIComponent(`books/search?q=${value}`)}`,
    );
  };

  const handleOnKeyDown = (e: any) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((prev) =>
        prev < suggestions.length - 1 ? prev + 1 : prev,
      );
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev > 0 ? prev - 1 : -1));
    } else if (e.key === "Enter") {
      if (selectedIndex >= 0) {
        handleSearchAction(suggestions[selectedIndex]);
      } else {
        handleSearchAction(query);
      }
      setShowSuggestions(false);
    } else if (e.key === "Escape") {
      setShowSuggestions(false);
    }
  };

  return (
    <div
      ref={suggestionsRef}
      className="relative w-full max-w-2xl mx-auto flex"
    >
      <div className="absolute transform translate-y-1/3 translate-x-2 pointer-events-none text-[#C7C6CB] z-10">
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
          <path d="m21 21-4.34-4.34" />
          <circle cx="11" cy="11" r="8" />
        </svg>
      </div>
      <input
        type="text"
        name="search"
        placeholder="Search"
        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-gray-400 "
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onFocus={() => setShowSuggestions(true)}
        onKeyDown={handleOnKeyDown}
      />
      {showSuggestions && suggestions.length > 0 && (
        <ul className="absolute mt-[45px] ml-0 w-full bg-white rounded-lg list-none z-50 overflow-x-hidden overflow-y-auto">
          {suggestions.map((item, index) => (
            <li
              key={index}
              onClick={() => {
                handleSearchAction(item);
              }}
              className={`p-2.5 cursor-pointer hover:bg-gray-200 ${index === selectedIndex && "bg-gray-200"}`}
            >
              {item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
