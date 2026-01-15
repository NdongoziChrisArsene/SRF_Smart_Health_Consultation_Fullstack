import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { Provider } from "react-redux";
import { Toaster } from "react-hot-toast";

import App from "./App";
import { store } from "./redux/store";
import { ThemeProvider } from "./context/ThemeContext";

import "./index.css"; // Tailwind / global styles

const rootElement = document.getElementById("root");

if (!rootElement) {
  throw new Error("Root element not found. Check index.html.");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <ThemeProvider>
          <App />
          <Toaster />
        </ThemeProvider>
      </BrowserRouter>
    </Provider>
  </React.StrictMode>
);
























