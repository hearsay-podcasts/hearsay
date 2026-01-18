import { env } from '$env/dynamic/private';

export const API_URL = env.API_URL || 'http://localhost:8000/api/v1';
export const IS_PRODUCTION = env.NODE_ENV === 'production';

export const COOKIE_CONFIG = {
	path: '/',
	httpOnly: true,
	secure: IS_PRODUCTION,
	sameSite: 'lax' as const,
	maxAge: 60 * 60 * 24 * 8 // 8 days (must match backend)
};
