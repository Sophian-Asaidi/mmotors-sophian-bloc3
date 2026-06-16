import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";

import App from "../App.jsx";

describe("Search", () => {
  beforeEach(() => {
    localStorage.clear();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => [
          {
            id: 1,
            brand: "Peugeot",
            model: "208",
            year: 2021,
            mileage: 38000,
            price: 13990,
            monthly_price: null,
            energy: "Essence",
            transmission: "Manuelle",
            mode: "sale",
            status: "available",
            created_at: "2026-01-01T00:00:00",
          },
        ],
      }),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  test("affiche la recherche et les véhicules", async () => {
    render(
      <MemoryRouter initialEntries={["/search"]}>
        <App />
      </MemoryRouter>,
    );

    expect(screen.getByRole("heading", { name: /recherche véhicules/i })).toBeInTheDocument();
    expect(await screen.findByText(/peugeot 208/i)).toBeInTheDocument();
  });
});

