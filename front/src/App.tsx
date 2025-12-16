import { BrowserRouter, Route, Routes } from "react-router";
import "./App.css";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import CategoriesPage from "./pages/CategoriesPage";
import BookListingPage from "./pages/BookListingPage";
import { AuthProvider } from "./services/AuthProvider";
import { apiClient } from "./services/api";
import { useEffect, useState } from "react";

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
  const [books, setBooks] = useState([]);
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      setBooks(
        await apiClient.request("books?limit=20", {
          method: "GET",
        }),
      );
      setCategories(
        await apiClient.request("classes", {
          method: "GET",
        }),
      );
    };

    fetchData();
  }, []);

  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
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
              <BookListingPage title="Historique" route="books?limit=20" />
            }
          />
          <Route
            path="/category/:id"
            element={<BookListingPage title="" />}
          ></Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
