export const SERVER_URL = process.env.REACT_APP_SERVER_URL;
export const accessToken = (): string | null =>
  sessionStorage.getItem("accessToken");
export const refreshToken = (): string | null =>
  sessionStorage.getItem("refreshToken");
export const expiresIn = (): number | null => {
  const duration = sessionStorage.getItem("expiresIn");
  return duration ? parseInt(duration) : null;
};
export const expireTime = (): number | null => {
  const time = sessionStorage.getItem("expireTime");
  return time ? parseInt(time) : null;
};
export const authCode = (): string | null =>
  new URLSearchParams(window.location.search).get("code");
