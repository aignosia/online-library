import { createContext, useState } from "react";
import { useNavigate } from "react-router";

interface AuthData {
  token: string;
  user: object | null;
  loginAction(data: object): void;
  logOut(): void;
}

const AuthContext = createContext<AuthData>({
  token: "",
  user: {},
  loginAction: () => {},
  logOut: () => {},
});

const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("site") || "");
  const navigate = useNavigate();

  const loginAction = async (data: URLSearchParams) => {
    data.forEach((e) => console.log(e));
    try {
      const response = await fetch("http://localhost:8000/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: data,
      });
      const res = await response.json();
      console.log(res);
      if (res) {
        setUser(res.user);
        setToken(res.token);
        localStorage.setItem("site", res.token);
        navigate("/home");
        return;
      }
      throw new Error(res.message);
    } catch (err) {
      console.log(err);
    }
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

export { AuthContext, AuthProvider };
