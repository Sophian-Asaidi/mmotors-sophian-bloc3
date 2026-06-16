import { Link } from "react-router-dom";

export default function VehicleCard({ vehicle }) {
  const isRental = vehicle.mode === "rental";
  const applicationType = isRental ? "rental" : "purchase";

  return (
    <article className="vehicle-card">
      <div>
        <span className={`badge ${isRental ? "badge-rental" : "badge-sale"}`}>
          {isRental ? "Location" : "Achat"}
        </span>
        <h3>
          {vehicle.brand} {vehicle.model}
        </h3>
        <p>
          {vehicle.year} · {vehicle.mileage.toLocaleString("fr-FR")} km · {vehicle.energy}
        </p>
        <p>{vehicle.transmission}</p>
      </div>
      <div className="vehicle-card__footer">
        <strong>
          {isRental
            ? `${vehicle.monthly_price?.toLocaleString("fr-FR")} €/mois`
            : `${vehicle.price?.toLocaleString("fr-FR")} €`}
        </strong>
        <Link className="button" to={`/applications/new?vehicleId=${vehicle.id}&type=${applicationType}`}>
          Déposer un dossier
        </Link>
      </div>
    </article>
  );
}

