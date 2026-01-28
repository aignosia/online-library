import { useEffect, useRef } from "react";

export default function useHandleOutsideClick(callback: () => void) {
  const ref = useRef<any>(null);
  useEffect(() => {
    const handleOutsideClick = (event: MouseEvent | TouchEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node))
        callback();
    };
    document.addEventListener("mousedown", handleOutsideClick);
    return () => document.removeEventListener("mousedown", handleOutsideClick);
  }, [callback]);
  return ref;
}
