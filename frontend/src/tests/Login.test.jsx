import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, test } from "vitest";

import App from "../App.jsx";

describe("Login", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test("affiche le formulaire de connexion", () => {
    render(
      <MemoryRouter initialEntries={["/login"]}>
        <App />
      </MemoryRouter>,
    );

    expect(screen.getByRole("heading", { name: /connexion/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toHaveValue("userLocal@Motors");
  });
});

