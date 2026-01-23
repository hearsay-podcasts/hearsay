export interface User {
	id: string;
	email: string;
	full_name: string | null;
	is_active: boolean;
}

export interface LoginCredentials {
	email: string;
	password: string;
}

export interface SignupData {
	email: string;
	password: string;
	full_name?: string;
}

export interface ApiError {
	detail: string;
}

export interface Podcast {
	id: string;
	title: string;
	author: string | null;
	description: string | null;
	cover_url: string | null;
	feed_url: string | null;
	is_featured: boolean;
	// Listen Notes fields
	listenotes_id: string | null;
	publisher: string | null;
	total_episodes: number | null;
	listen_score: number | null;
	genre_ids: string | null;
	listenotes_url: string | null;
	// iTunes artwork fields
	itunes_id: string | null;
	cover_url_sm: string | null;
	cover_url_md: string | null;
	cover_url_lg: string | null;
}

export interface PodcastList {
	podcasts: Podcast[];
	count: number;
}
