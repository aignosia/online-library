import { BrowserRouter, Route, Routes } from "react-router";
import "./App.css";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import CategoriesPage from "./pages/CategoriesPage";
import BookListingPage from "./pages/BookListingPage";
import { AuthProvider } from "./services/AuthProvider";

export interface Book {
  title: string;
  author: string;
}

function App() {
  const categories = [
    "Litérature",
    "Science et technologie",
    "Histoire",
    "Sciences sociales et société",
    "Art et culture",
    "Religion et philosophie",
    "Santé et médecine",
    "Éducation et références",
    "Mode de vie et loisirs",
  ];
  const books: Array<Book> = [
    {
      title: "An Inquiry into the Nature and Causes of the Wealth of Nations",
      author: "Adam Smith",
    },
    {
      title: "An Inquiry into the Nature and Causes of the Wealth of Nations",
      author: "Adam Smith",
    },
    {
      title: "An Inquiry into the Nature and Causes of the Wealth of Nations",
      author: "Adam Smith",
    },
    {
      title: "An Inquiry into the Nature and Causes of the Wealth of Nations",
      author: "Adam Smith",
    },
    {
      title: "An Inquiry into the Nature and Causes of the Wealth of Nations",
      author: "Adam Smith",
    },
    {
      title: "An Inquiry into the Nature and Causes of the Wealth of Nations",
      author: "Adam Smith",
    },
  ];
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
            element={<BookListingPage title="Historique" books={books} />}
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
