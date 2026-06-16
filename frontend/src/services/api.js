export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const headers = new Headers(options.headers || {});
  const isFormData = typeof FormData !== "undefined" && options.body instanceof FormData;

  if (!isFormData && options.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const token = localStorage.getItem("token");
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!response.ok) {
    let message = "Une erreur est survenue";
    try {
      const data = await response.json();
      message = data.detail || message;
    } catch {
      message = response.statusText || message;
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    return null;
  }
  return response.json();
}

export const api = {
  login: (payload) => request("/auth/login", { method: "POST", body: JSON.stringify(payload) }),
  register: (payload) => request("/auth/register", { method: "POST", body: JSON.stringify(payload) }),
  getVehicles: ({ mode, search } = {}) => {
    const params = new URLSearchParams();
    if (mode) params.set("mode", mode);
    if (search) params.set("search", search);
    return request(`/vehicles${params.toString() ? `?${params}` : ""}`);
  },
  getMyApplications: () => request("/applications/me"),
  createApplication: (formData) => request("/applications", { method: "POST", body: formData }),
  createVehicle: (payload) => request("/admin/vehicles", { method: "POST", body: JSON.stringify(payload) }),
  switchVehicle: (vehicleId) => request(`/admin/vehicles/${vehicleId}/switch`, { method: "PATCH" }),
  getAdminApplications: () => request("/admin/applications"),
  updateApplicationStatus: (applicationId, payload) =>
    request(`/admin/applications/${applicationId}/status`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    }),
  health: () => request("/health"),
};

