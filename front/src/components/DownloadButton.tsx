import React, { useState, useEffect, useRef } from "react";
import {
  HiChevronDown,
  HiDownload,
  HiOutlineDocumentText,
  HiOutlineBookOpen,
  HiOutlineCode,
} from "react-icons/hi";
import {
  AiOutlineFileText,
  AiOutlineFileZip,
  AiOutlineLoading3Quarters,
} from "react-icons/ai";
import type { BookFile } from "../pages/BookInfoPage";
import { RiBook3Line, RiBookFill } from "react-icons/ri";
import { FaTabletAlt } from "react-icons/fa";

interface DownloadButtonProps {
  options?: Array<BookFile>;
  color: string;
  hoverColor: string;
}

export default function DownloadButton(props: DownloadButtonProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleOnClick = () => {
    if (props.options && props.options.length > 0) {
      setIsOpen(!isOpen);
      return;
    }

    setLoading(true);
  };

  const getIcon = (format: string) => {
    switch (format) {
      case "epub_no_img": // Ancien epub sans image
        return <HiOutlineBookOpen className="w-5 h-5 text-slate-500" />;

      case "epub_img": // Ancien epub avec image
        return <RiBookFill className="w-5 h-5 text-blue-500" />;

      case "epub3_img": // Epub3 avec image
        return <RiBook3Line className="w-5 h-5 text-indigo-600" />;

      case "kindle": // Kindle moderne
        return <FaTabletAlt className="w-5 h-5 text-orange-500" />;

      case "kindle_legacy": // Ancien kindle
        return <FaTabletAlt className="w-5 h-5 text-gray-400 opacity-70" />;

      case "text": // Plain text
        return <AiOutlineFileText className="w-5 h-5 text-gray-600" />;

      case "html_zip": // HTML à l'intérieur d'un ZIP
        return (
          <div className="relative">
            <AiOutlineFileZip className="w-5 h-5 text-yellow-600" />
            <HiOutlineCode className="w-3 h-3 text-white absolute bottom-0 right-0 bg-yellow-600 rounded-full" />
          </div>
        );

      default:
        return <HiOutlineDocumentText className="w-5 h-5 text-gray-400" />;
    }
  };

  return (
    <div className="relative inline-block text-left" ref={menuRef}>
      <button
        onClick={handleOnClick}
        disabled={loading}
        style={
          {
            "--btn-color": props.color,
            "--btn-hover-color": props.hoverColor,
          } as React.CSSProperties
        }
        className="bg-(--btn-color) hover:bg-(--btn-hover-color) w-45 md:w-64 flex md:gap-2 items-center justify-center font-medium text-gray-700 hover:text-gray-900 px-6 py-2 rounded-md transition-colors"
      >
        <div className="flex items-center md:gap-2">
          {loading ? (
            <AiOutlineLoading3Quarters className="animate-spin" />
          ) : (
            <HiDownload size={18} />
          )}
          <span className="font-medium">Download</span>
        </div>
        <HiChevronDown
          className={`transition-transform duration-300 ${isOpen ? "rotate-180" : ""}`}
        />
      </button>

      {isOpen && (
        <div className="absolute left-0 mt-2 w-45 md:w-64 origin-top-left rounded-xl bg-white shadow-2xl ring-1 ring-black/5 overflow-hidden z-50">
          <div className="bg-gray-50 px-4 py-2 border-b border-gray-100">
            <span className="text-[10px] font-bold uppercase tracking-wider text-gray-400">
              Options disponibles
            </span>
          </div>
          <div className="py-1">
            {props.options &&
              props.options.map((option) => (
                <a
                  key={option.id}
                  href={option.location}
                  className="group flex items-center px-4 py-3 hover:bg-blue-50 transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  <div className="mr-3 p-2 bg-gray-50 rounded-lg group-hover:bg-white transition-colors">
                    {getIcon(option.type)}
                  </div>
                  <div className="flex flex-col">
                    <span className="text-sm text-gray-700 group-hover:text-blue-700">
                      {option.label}
                    </span>
                  </div>
                </a>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}
