export default function LoginPage() {
  return (
    <div className="min-h-screen bg-[#f8f5f1] flex flex-col">
      <header className="flex justify-between items-center px-10 py-6">
        <div className="flex flex-col">
          <h1 className="text-2xl font-bold text-gray-900">
            <span className="text-[#f4b759]">Online</span>{" "}
            <span className="text-gray-700">Library</span>
          </h1>
        </div>
        <div className="flex items-center gap-6">
          <button className="bg-[#f4b759] hover:bg-[#f2a73e] font-medium text-gray-700 hover:text-gray-900 px-6 py-2 rounded-md transition-colors">
            Sign up
          </button>
          {/*<button className="bg-[#f4b759] hover:bg-[#f2a73e] text-black font-medium px-5 py-2 rounded-md transition-colors">
            Request Demo
          </button>*/}
        </div>
      </header>

      <main className="grow flex justify-center items-center px-4">
        <div className="relative flex flex-col md:flex-row items-center gap-12">
          <div className="bg-white shadow-xl rounded-3xl p-10 w-[450px]">
            <h2 className="text-2xl font-semibold text-center mb-2">Login</h2>
            <p className="text-gray-500 text-lg text-center mb-12">
              Hey, enter your details to get sign in to your account
            </p>

            <form className="flex flex-col">
              <input
                type="text"
                placeholder="Enter Email"
                className="w-full border border-gray-200 rounded-md px-4 py-2 mb-8 focus:outline-none focus:ring-2 focus:ring-yellow-400"
              />
              <input
                type="password"
                placeholder="Password"
                className="w-full border border-gray-200 rounded-md mb-4 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-yellow-400"
              />

              <p className="text-sm text-gray-500 mb-12">
                Having trouble in sign in?
              </p>

              <button
                type="submit"
                className="bg-[#f4b759] hover:bg-[#f2a73e] text-black font-medium py-2 rounded-md transition-colors"
              >
                Sign in
              </button>
            </form>

            <div className="my-4 flex items-center justify-center gap-2 text-gray-400">
              <span className="h-px w-10 bg-gray-300"></span>
              <span className="text-sm">
                Don't have an account?{" "}
                <a href="/">
                  <u>Sign up</u>
                </a>
              </span>
              <span className="h-px w-10 bg-gray-300"></span>
            </div>

            {/*<div className="flex justify-center gap-4">
              <button className="border border-gray-200 rounded-md p-2 hover:bg-gray-50">
                <FcGoogle size={20} />
              </button>
              <button className="border border-gray-200 rounded-md p-2 hover:bg-gray-50">
                <FaApple size={20} />
              </button>
              <button className="border border-gray-200 rounded-md p-2 hover:bg-gray-50 text-[#1877f2]">
                <FaFacebookF size={20} />
              </button>
            </div>*/}
          </div>
        </div>
      </main>
    </div>
  );
}
