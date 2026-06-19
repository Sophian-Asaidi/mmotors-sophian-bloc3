const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

async function request(path, options = {}) {
  const { token, body, headers = {}, ...rest } = options;
  const finalHeaders = { ...headers };

  if (token) finalHeaders.Authorization = `Bearer ${token}`;
  if (body && !(body instanceof FormData)) finalHeaders['Content-Type'] = 'application/json';

  const response = await fetch(`${API_URL}${path}`, {
    ...rest,
    headers: finalHeaders,
    body: body instanceof FormData ? body : body ? JSON.stringify(body) : undefined,
  });

  const contentType = response.headers.get('content-type') || '';
  const data = contentType.includes('application/json') ? await response.json() : await response.text();
  if (!response.ok) {
    const message = typeof data === 'object' ? data.detail || 'Erreur API' : data;
    throw new Error(message);
  }
  return data;
}

export const api = {
  url: API_URL,
  login: (email, password) => request('/auth/login', { method: 'POST', body: { email, password } }),
  register: (email, password) => request('/auth/register', { method: 'POST', body: { email, password } }),
  me: (token) => request('/auth/me', { token }),
  vehicles: (mode = '') => request(`/vehicles${mode ? `?mode=${mode}` : ''}`),
  submitApplication: (token, formData) => request('/applications', { method: 'POST', token, body: formData }),
  myApplications: (token) => request('/applications/me', { token }),
  adminApplications: (token) => request('/admin/applications', { token }),
  decideApplication: (token, id, status, admin_comment) => request(`/admin/applications/${id}/status`, {
    method: 'PATCH', token, body: { status, admin_comment }
  }),
  createVehicle: (token, vehicle) => request('/admin/vehicles', { method: 'POST', token, body: vehicle }),
  changeVehicleMode: (token, id, payload) => request(`/admin/vehicles/${id}/mode`, { method: 'PATCH', token, body: payload }),
  health: () => request('/health'),
  metrics: () => request('/metrics'),
  alertTest: () => request('/health/alert-test?reason=frontend-test', { method: 'POST' }),
};
