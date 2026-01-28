import { BrowserRouter, Navigate, Route, Routes } from "react-router";
import "./App.css";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import CategoriesPage from "./pages/CategoriesPage";
import BookListingPage from "./pages/BookListingPage";
import { AuthProvider } from "./services/AuthProvider";
import BookInfoPage from "./pages/BookInfoPage";

export interface Author {
  id: number;
  firstname: string;
  lastname: string;
  birth_year: string;
  death_year: string;
  fuller_name: string;
}

export interface Book {
  id: number;
  title: string;
  authors: Array<Author>;
  pubyear: number;
  cover: string | null;
}

export interface Subclass {
  id: number;
  name: string;
}

export interface Categorie {
  id: number;
  name: string;
  subclasses: Array<Subclass>;
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Navigate to="/home" replace />}></Route>
          <Route path="/home" element={<HomePage />} />
          <Route path="/login" element={<LoginPage type="login" />} />
          <Route path="/signup" element={<LoginPage type="signup" />} />
          <Route path="/categories" element={<CategoriesPage />} />
          <Route
            path="/history"
            element={
              <BookListingPage
                key="history"
                title="Historique"
                route="users/me/books"
                authorization={true}
                hasPagination={true}
              />
            }
          />
          <Route
            path="/main-category/:id"
            element={
              <BookListingPage
                key="main-cat"
                authorization={false}
                hasPagination={true}
              />
            }
          ></Route>
          <Route
            path="/category/:id"
            element={
              <BookListingPage
                key="cat"
                authorization={false}
                hasPagination={true}
              />
            }
          ></Route>
          <Route path="/book/:id" element={<BookInfoPage />}></Route>
          <Route
            path="/search"
            element={
              <BookListingPage
                key="search"
                authorization={false}
                hasPagination={true}
              />
            }
          ></Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
