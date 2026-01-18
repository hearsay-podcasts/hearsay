import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { API_URL, COOKIE_CONFIG } from '$lib/server/config';

export const load: PageServerLoad = async ({ locals }) => {
	// Redirect to dashboard if already logged in
	if (locals.user) {
		throw redirect(303, '/dashboard');
	}
};

export const actions: Actions = {
	default: async ({ request, cookies }) => {
		const formData = await request.formData();
		const email = formData.get('email') as string;
		const password = formData.get('password') as string;

		if (!email || !password) {
			return fail(400, { error: 'Email and password are required' });
		}

		try {
			const response = await fetch(`${API_URL}/auth/login`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, password })
			});

			if (!response.ok) {
				const error = await response.json();
				return fail(response.status, { error: error.detail || 'Login failed' });
			}

			// Extract the cookie from FastAPI response and set it in SvelteKit
			const setCookieHeader = response.headers.get('set-cookie');
			if (setCookieHeader) {
				// Parse the cookie value
				const cookieMatch = setCookieHeader.match(/access_token=([^;]+)/);
				if (cookieMatch) {
					const tokenValue = cookieMatch[1];
					cookies.set('access_token', tokenValue, COOKIE_CONFIG);
				}
			}
		} catch (error) {
			console.error('Login error:', error);
			return fail(500, { error: 'An unexpected error occurred' });
		}

		throw redirect(303, '/dashboard');
	}
};
