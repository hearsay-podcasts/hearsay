import type { Handle } from '@sveltejs/kit';
import type { User } from '$lib/types';
import { API_URL, COOKIE_CONFIG } from '$lib/server/config';

export const handle: Handle = async ({ event, resolve }) => {
	const token = event.cookies.get('access_token');

	if (token) {
		try {
			// Verify token by calling the /auth/me endpoint
			const response = await fetch(`${API_URL}/auth/me`, {
				headers: {
					Cookie: `access_token=${token}`
				}
			});

			if (response.ok) {
				const user: User = await response.json();
				event.locals.user = user;
			} else {
				// Token is invalid, clear the cookie
				event.cookies.delete('access_token', {
					path: COOKIE_CONFIG.path,
					secure: COOKIE_CONFIG.secure,
					sameSite: COOKIE_CONFIG.sameSite
				});
				event.locals.user = null;
			}
		} catch (error) {
			// API error, continue without user
			console.error('Auth check failed:', error);
			event.locals.user = null;
		}
	} else {
		event.locals.user = null;
	}

	return resolve(event);
};
