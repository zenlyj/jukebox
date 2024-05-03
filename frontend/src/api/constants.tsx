export const SERVER_URL = process.env.REACT_APP_SERVER_URL;
export const authCode = (): string | null =>
  new URLSearchParams(window.location.search).get("code");
