import { useState } from "react";
import { useNavigate } from "react-router";
import { AuthContext } from "./AuthContext";

const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("site") || "");
  const navigate = useNavigate();

  const loginAction = async (data: URLSearchParams) => {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: data,
    });
    const res = await response.json();
    if (response.ok) {
      setUser(res.user);
      setToken(res.access_token);
      localStorage.setItem("site", res.access_token);
      navigate("/home");
      return;
    }
    throw new Error(res.message);
  };

  const logOut = () => {
    setUser(null);
    setToken("");
    localStorage.removeItem("site");
    navigate("/login");
  };
  return (
    <AuthContext.Provider value={{ token, user, loginAction, logOut }}>
      {children}{" "}
    </AuthContext.Provider>
  );
};

export { AuthProvider };
