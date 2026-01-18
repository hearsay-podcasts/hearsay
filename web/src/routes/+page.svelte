<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<div class="home">
	<h1>Welcome to Hearsay</h1>
	<p class="tagline">Your podcast platform</p>

	{#if data.user}
		<div class="logged-in">
			<p>You're logged in as <strong>{data.user.email}</strong></p>
			<a href="/dashboard" class="button">Go to Dashboard</a>
		</div>
	{:else}
		<div class="cta">
			<p>Get started by creating an account or logging in.</p>
			<div class="buttons">
				<a href="/signup" class="button primary">Sign Up</a>
				<a href="/login" class="button">Login</a>
			</div>
		</div>
	{/if}
</div>

<style>
	.home {
		text-align: center;
		padding: 4rem 2rem;
	}

	h1 {
		font-size: 2.5rem;
		color: #1a1a2e;
		margin-bottom: 0.5rem;
	}

	.tagline {
		font-size: 1.25rem;
		color: #666;
		margin-bottom: 2rem;
	}

	.logged-in,
	.cta {
		margin-top: 2rem;
	}

	.buttons {
		display: flex;
		gap: 1rem;
		justify-content: center;
		margin-top: 1rem;
	}

	.button {
		display: inline-block;
		padding: 0.75rem 1.5rem;
		border-radius: 4px;
		text-decoration: none;
		font-weight: 500;
		border: 2px solid #1a1a2e;
		color: #1a1a2e;
		background: white;
		transition: all 0.2s;
	}

	.button:hover {
		background: #1a1a2e;
		color: white;
	}

	.button.primary {
		background: #1a1a2e;
		color: white;
	}

	.button.primary:hover {
		background: #16213e;
		border-color: #16213e;
	}
</style>
