import { BrowserRouter, Navigate, Route, Routes } from "react-router";
import "./App.css";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import CategoriesPage from "./pages/CategoriesPage";
import BookListingPage from "./pages/BookListingPage";
import { AuthProvider } from "./services/AuthProvider";
import { apiClient } from "./services/api";
import { useContext, useEffect, useState } from "react";
import BookInfoPage from "./pages/BookInfoPage";
import { AuthContext } from "./services/AuthContext";

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
  const auth = useContext(AuthContext);
  const [books, setBooks] = useState(new Array<Book>());
  const [categories, setCategories] = useState(new Array<Categorie>());

  useEffect(() => {
    const fetchData = async () => {
      const limit = 20;
      let endpoint = "";
      if (auth.user) endpoint = `users/me/books/recommendations?limit=${limit}`;
      else endpoint = `books/popular?limit=${limit}`;
      setBooks(
        await apiClient.request(endpoint, {
          method: "GET",
        }),
      );
      const fetchedCategories = await apiClient.request("classes", {
        method: "GET",
      });
      fetchedCategories.sort((a: Categorie, b: Categorie) =>
        a.name.localeCompare(b.name),
      );
      setCategories(fetchedCategories);
    };

    fetchData();
  }, [auth.user]);

  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Navigate to="/home" replace />}></Route>
          <Route
            path="/home"
            element={<HomePage categories={categories} books={books} />}
          />
          <Route path="/login" element={<LoginPage type="login" />} />
          <Route path="/signup" element={<LoginPage type="signup" />} />
          <Route
            path="/categories"
            element={<CategoriesPage categories={categories} />}
          />
          <Route
            path="/history"
            element={
              <BookListingPage
                title="Historique"
                route="users/me/books?limit=20"
                authorization={true}
              />
            }
          />
          <Route
            path="/main-category/:id"
            element={<BookListingPage authorization={false} />}
          ></Route>
          <Route
            path="/category/:id"
            element={<BookListingPage authorization={false} />}
          ></Route>
          <Route path="/book/:id" element={<BookInfoPage />}></Route>
          <Route
            path="/search"
            element={<BookListingPage authorization={false} />}
          ></Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
