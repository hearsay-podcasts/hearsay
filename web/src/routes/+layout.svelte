<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import type { LayoutData } from './$types';

	let { data, children }: { data: LayoutData; children: any } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<nav>
	<a href="/">Hearsay</a>
	<div>
		{#if data.user}
			<span>Welcome, {data.user.email}</span>
			<a href="/dashboard">Dashboard</a>
			<form method="POST" action="/logout" style="display: inline;">
				<button type="submit">Logout</button>
			</form>
		{:else}
			<a href="/login">Login</a>
			<a href="/signup">Sign Up</a>
		{/if}
	</div>
</nav>

<main>
	{@render children()}
</main>

<style>
	nav {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem 2rem;
		background: #1a1a2e;
		color: white;
	}

	nav a {
		color: white;
		text-decoration: none;
		margin-left: 1rem;
	}

	nav a:hover {
		text-decoration: underline;
	}

	nav button {
		background: transparent;
		border: 1px solid white;
		color: white;
		padding: 0.25rem 0.5rem;
		cursor: pointer;
		margin-left: 1rem;
	}

	nav button:hover {
		background: white;
		color: #1a1a2e;
	}

	main {
		padding: 2rem;
		max-width: 800px;
		margin: 0 auto;
	}
</style>
