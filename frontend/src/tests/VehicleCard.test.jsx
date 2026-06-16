import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, test } from "vitest";

import VehicleCard from "../components/VehicleCard.jsx";

describe("VehicleCard", () => {
  test("affiche les informations du véhicule", () => {
    render(
      <MemoryRouter>
        <VehicleCard
          vehicle={{
            id: 1,
            brand: "Renault",
            model: "Clio",
            year: 2022,
            mileage: 24500,
            price: null,
            monthly_price: 289,
            energy: "Hybride",
            transmission: "Automatique",
            mode: "rental",
          }}
        />
      </MemoryRouter>,
    );

    expect(screen.getByRole("heading", { name: /renault clio/i })).toBeInTheDocument();
    expect(screen.getByText(/location/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /déposer un dossier/i })).toBeInTheDocument();
  });
});

