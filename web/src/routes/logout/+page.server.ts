import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import { API_URL, COOKIE_CONFIG } from '$lib/server/config';

export const actions: Actions = {
	default: async ({ cookies }) => {
		// Call backend logout to clear cookie there too
		try {
			await fetch(`${API_URL}/auth/logout`, {
				method: 'POST',
				headers: {
					Cookie: `access_token=${cookies.get('access_token')}`
				}
			});
		} catch (error) {
			console.error('Logout API error:', error);
		}

		// Clear the cookie on the SvelteKit side
		cookies.delete('access_token', {
			path: COOKIE_CONFIG.path,
			secure: COOKIE_CONFIG.secure,
			sameSite: COOKIE_CONFIG.sameSite
		});

		throw redirect(303, '/');
	}
};
