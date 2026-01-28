import { useEffect, useState, type ReactNode } from "react";
import { useNavigate } from "react-router";
import { AuthContext } from "./AuthContext";

const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState(
    localStorage.getItem("user")
      ? JSON.parse(localStorage.getItem("user") || "{}")
      : null,
  );
  const [token, setToken] = useState(localStorage.getItem("site") || "");
  const navigate = useNavigate();

  useEffect(() => {
    const testAuthentication = async () => {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/users/me`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.status === 401) {
        setUser(null);
        localStorage.removeItem("user");
        setToken("");
        localStorage.removeItem("site");
        navigate("/login");
      }
    };
    if (localStorage.getItem("user") || localStorage.getItem("site"))
      testAuthentication();
  }, [navigate, token]);

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
      localStorage.setItem("user", JSON.stringify(res.user));
      setToken(res.access_token);
      localStorage.setItem("site", res.access_token);
      navigate("/home");
      return;
    }
    throw new Error(res.message);
  };

  const logOut = () => {
    setUser(null);
    localStorage.removeItem("user");
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
