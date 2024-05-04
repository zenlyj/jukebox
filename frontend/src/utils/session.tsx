import { UserProfile } from "../components/models/UserProfile.tsx";

const ACCESS_TOKEN_KEY = "accessToken";
const REFRESH_TOKEN_KEY = "refreshToken";
const TOKEN_EXPIRES_IN_KEY = "tokenExpiresIn";
const TOKEN_EXPIRE_TIME_KEY = "tokenExpireTime";
const USER_NAME_KEY = "userName";
const USER_ID_KEY = "userId";

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

export const getUserInfo = (): UserProfile | null => {
  const name = sessionStorage.getItem(USER_NAME_KEY);
  const userId = sessionStorage.getItem(USER_ID_KEY);
  if (!name || !userId) {
    return null;
  }
  return {
    name: name,
    userId: userId,
  };
};
export const setUserInfo = (
  name: string | null,
  userId: string | null
): void => {
  if (name && userId) {
    sessionStorage.setItem(USER_NAME_KEY, name);
    sessionStorage.setItem(USER_ID_KEY, userId);
  }
};
