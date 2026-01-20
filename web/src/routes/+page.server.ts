import type { PageServerLoad } from './$types';
import { API_URL } from '$lib/server/config';
import type { PodcastList } from '$lib/types';

export const load: PageServerLoad = async ({ fetch }) => {
	let popularPodcasts: PodcastList = { podcasts: [], count: 0 };

	try {
		const response = await fetch(`${API_URL}/podcasts/popular?limit=4`);
		if (response.ok) {
			popularPodcasts = await response.json();
		}
	} catch {
		// Silently fail - landing page should still render without podcasts
	}

	return {
		popularPodcasts
	};
};
