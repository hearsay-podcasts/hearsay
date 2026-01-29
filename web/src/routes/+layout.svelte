<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import type { LayoutData } from './$types';
	import type { Snippet } from 'svelte';

	let { data, children }: { data: LayoutData; children: Snippet } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<nav>
	<a href="/" class="logo">hearsay</a>
	<div class="nav-links">
		{#if data.user}
			<span class="welcome">Welcome, {data.user.email}</span>
			<a href="/dashboard">Dashboard</a>
			<form method="POST" action="/logout" style="display: inline;">
				<button type="submit">Logout</button>
			</form>
		{:else}
			<a href="/login">Sign in</a>
			<a href="/signup">Create account</a>
		{/if}
	</div>
</nav>

<main>
	{@render children()}
</main>

<style>
	:global(body) {
		margin: 0;
		font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
	}

	nav {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem 3rem;
		background: #1a1a2e;
		color: white;
	}

	.logo {
		font-family: 'Instrument Serif', Georgia, serif;
		font-size: 1.5rem;
		font-weight: 400;
		color: white;
		text-decoration: none;
		letter-spacing: -0.02em;
	}

	.logo:hover {
		text-decoration: none;
		opacity: 0.9;
	}

	.nav-links {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.nav-links a {
		color: rgba(255, 255, 255, 0.85);
		text-decoration: none;
		padding: 0.5rem 1rem;
		font-size: 0.875rem;
		font-weight: 500;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		transition: color 0.2s;
	}

	.nav-links a:hover {
		color: white;
		text-decoration: none;
	}

	.welcome {
		font-size: 0.875rem;
		color: rgba(255, 255, 255, 0.7);
		margin-right: 0.5rem;
	}

	nav button {
		background: transparent;
		border: 1px solid rgba(255, 255, 255, 0.5);
		color: white;
		padding: 0.5rem 1rem;
		font-size: 0.875rem;
		font-weight: 500;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		cursor: pointer;
		border-radius: 4px;
		transition: all 0.2s;
	}

	nav button:hover {
		background: white;
		color: #1a1a2e;
		border-color: white;
	}

	main {
		min-height: calc(100vh - 60px);
	}

	@media (max-width: 768px) {
		nav {
			padding: 1rem 1.5rem;
		}

		.nav-links a {
			padding: 0.5rem 0.75rem;
		}

		.welcome {
			display: none;
		}
	}
</style>
