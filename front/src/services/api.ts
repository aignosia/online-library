export const apiClient = {
  async request(endpoint: string, options: RequestInit = {}) {
    const response = await fetch(`http://localhost:8000/${endpoint}`, options);

    if (!response.ok) {
      throw new Error(await response.text());
    }

    return response.json();
  },
};
