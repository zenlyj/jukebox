export const SERVER_URL = process.env.REACT_APP_SERVER_URL;
export const accessToken = (): string | null =>
  sessionStorage.getItem("accessToken");
export const refreshToken = (): string | null =>
  sessionStorage.getItem("refreshToken");
export const authCode = (): string | null =>
  new URLSearchParams(window.location.search).get("code");
