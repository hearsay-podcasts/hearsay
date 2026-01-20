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
	feed_url: string;
	is_featured: boolean;
}

export interface PodcastList {
	podcasts: Podcast[];
	count: number;
}
