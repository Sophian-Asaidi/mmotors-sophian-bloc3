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

async function downloadAdminDocument(token, document) {
  const response = await fetch(`${API_URL}/admin/documents/${document.id}/download`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Impossible de télécharger le document");
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);

  const link = window.document.createElement('a');
  link.href = url;
  link.download = document.filename || 'document';
  link.click();

  window.URL.revokeObjectURL(url);
}

export const api = {
  url: API_URL,

  login: (email, password) => request('/auth/login', {
    method: 'POST',
    body: { email, password },
  }),

  register: (email, password) => request('/auth/register', {
    method: 'POST',
    body: { email, password },
  }),

  me: (token) => request('/auth/me', { token }),

  vehicles: (mode = '') => request(`/vehicles${mode ? `?mode=${mode}` : ''}`),

  submitApplication: (token, formData) => request('/applications', {
    method: 'POST',
    token,
    body: formData,
  }),

  myApplications: (token) => request('/applications/me', { token }),

  adminApplications: (token) => request('/admin/applications', { token }),

  adminApplicationDetail: (token, id) => request(`/admin/applications/${id}`, { token }),

  updateClientComment: (token, id, admin_comment) => request(`/admin/applications/${id}/client-comment`, {
    method: 'PATCH',
    token,
    body: { admin_comment },
  }),

  addApplicationDocuments: (token, id, formData) => request(`/applications/${id}/documents`, {
    method: 'POST',
    token,
    body: formData,
  }),

  updateInternalComment: (token, id, internal_comment) => request(`/admin/applications/${id}/internal-comment`, {
    method: 'PATCH',
    token,
    body: { internal_comment },
  }),

  decideApplication: (token, id, status, admin_comment) => request(`/admin/applications/${id}/status`, {
    method: 'PATCH',
    token,
    body: { status, admin_comment },
  }),

  createVehicle: (token, vehicle) => request('/admin/vehicles', {
    method: 'POST',
    token,
    body: vehicle,
  }),

  changeVehicleMode: (token, id, payload) => request(`/admin/vehicles/${id}/mode`, {
    method: 'PATCH',
    token,
    body: payload,
  }),

  downloadAdminDocument,

  health: () => request('/health'),

  metrics: () => request('/metrics'),

  alertTest: () => request('/health/alert-test?reason=frontend-test', {
    method: 'POST',
  }),
};