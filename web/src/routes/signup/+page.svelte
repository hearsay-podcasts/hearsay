<script lang="ts">
	import { enhance } from '$app/forms';
	import type { ActionData } from './$types';

	let { form }: { form: ActionData } = $props();

	let loading = $state(false);
</script>

<div class="auth-container">
	<h1>Sign Up</h1>

	<form
		method="POST"
		use:enhance={() => {
			loading = true;
			return async ({ update }) => {
				loading = false;
				await update();
			};
		}}
	>
		<div class="form-group">
			<label for="email">Email</label>
			<input type="email" id="email" name="email" required disabled={loading} />
		</div>

		<div class="form-group">
			<label for="full_name">Full Name (optional)</label>
			<input type="text" id="full_name" name="full_name" disabled={loading} />
		</div>

		<div class="form-group">
			<label for="password">Password</label>
			<input
				type="password"
				id="password"
				name="password"
				required
				minlength="8"
				disabled={loading}
			/>
		</div>

		{#if form?.error}
			<div class="error">{form.error}</div>
		{/if}

		<button type="submit" disabled={loading}>
			{loading ? 'Creating account...' : 'Sign Up'}
		</button>
	</form>

	<p>Already have an account? <a href="/login">Login</a></p>
</div>

<style>
	.auth-container {
		max-width: 400px;
		margin: 2rem auto;
		padding: 2rem;
	}

	h1 {
		margin-bottom: 1.5rem;
	}

	.form-group {
		margin-bottom: 1rem;
	}

	label {
		display: block;
		margin-bottom: 0.25rem;
		font-weight: 500;
	}

	input {
		width: 100%;
		padding: 0.5rem;
		border: 1px solid #ccc;
		border-radius: 4px;
		font-size: 1rem;
	}

	input:disabled {
		background: #f5f5f5;
	}

	.error {
		color: #dc3545;
		background: #f8d7da;
		padding: 0.5rem;
		border-radius: 4px;
		margin-bottom: 1rem;
	}

	button {
		width: 100%;
		padding: 0.75rem;
		background: #1a1a2e;
		color: white;
		border: none;
		border-radius: 4px;
		font-size: 1rem;
		cursor: pointer;
	}

	button:hover:not(:disabled) {
		background: #16213e;
	}

	button:disabled {
		opacity: 0.7;
		cursor: not-allowed;
	}

	p {
		margin-top: 1rem;
		text-align: center;
	}

	a {
		color: #1a1a2e;
	}
</style>
