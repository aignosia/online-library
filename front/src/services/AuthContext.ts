import { createContext } from "react";

interface User {
  username: string;
  full_name: string;
  is_active: boolean;
}

interface AuthData {
  token: string;
  user: User | null;
  loginAction(data: object): void;
  logOut(): void;
}

const AuthContext = createContext<AuthData>({
  token: "",
  user: null,
  loginAction: () => {},
  logOut: () => {},
});

export { AuthContext };
