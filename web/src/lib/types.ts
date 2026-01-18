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
