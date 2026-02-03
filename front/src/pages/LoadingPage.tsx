import { ScaleLoader } from "react-spinners";

export function LoadingPage() {
  return (
    <>
      <div className="bg-[#f8f5f1] h-screen flex flex-col items-center justify-center">
        <p className="text-gray-700 mb-3 text-xl">Loading...</p>
        <ScaleLoader className="text-gray-700" />
      </div>
    </>
  );
}
