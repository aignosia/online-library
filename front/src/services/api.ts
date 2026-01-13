export const apiClient = {
  async request(endpoint: string, options: RequestInit = {}) {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/${endpoint}`,
      options,
    );

    if (!response.ok) {
      throw new Error(await response.text());
    }

    return response.json();
  },
};
