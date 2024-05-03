const ACCESS_TOKEN_KEY = "accessToken";
const REFRESH_TOKEN_KEY = "refreshToken";
const TOKEN_EXPIRES_IN_KEY = "tokenExpiresIn";
const TOKEN_EXPIRE_TIME_KEY = "tokenExpireTime";

export const getAccessToken = (): string | null =>
  sessionStorage.getItem(ACCESS_TOKEN_KEY);
export const setAccessToken = (accessToken: string | null): void => {
  if (accessToken) {
    sessionStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  }
};

export const getRefreshToken = (): string | null =>
  sessionStorage.getItem(REFRESH_TOKEN_KEY);
export const setRefreshToken = (refreshToken: string | null): void => {
  if (refreshToken) {
    sessionStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  }
};

export const getTokenExpiresIn = (): number => {
  const duration = sessionStorage.getItem(TOKEN_EXPIRES_IN_KEY);
  return duration ? parseInt(duration) : 0;
};
export const setTokenExpiresIn = (expiresIn: number | null): void => {
  if (expiresIn) {
    sessionStorage.setItem(TOKEN_EXPIRES_IN_KEY, expiresIn.toString());
  }
};

export const getTokenExpireTime = (): number => {
  const time = sessionStorage.getItem(TOKEN_EXPIRE_TIME_KEY);
  return time ? parseInt(time) : 0;
};
export const setTokenExpireTime = (expireTime: number | null): void => {
  if (expireTime) {
    sessionStorage.setItem(TOKEN_EXPIRE_TIME_KEY, expireTime.toString());
  }
};
