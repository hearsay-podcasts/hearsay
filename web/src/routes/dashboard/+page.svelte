<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<div class="dashboard">
	<h1>Dashboard</h1>

	<div class="user-info">
		<h2>Welcome back!</h2>
		<p><strong>Email:</strong> {data.user?.email}</p>
		{#if data.user?.full_name}
			<p><strong>Name:</strong> {data.user.full_name}</p>
		{/if}
		<p><strong>Account ID:</strong> {data.user?.id}</p>
	</div>

	<div class="content">
		<p>You're logged in and viewing a protected page.</p>
		<p>This is where your podcast content will appear.</p>
	</div>
</div>

<style>
	.dashboard {
		max-width: 800px;
		margin: 0 auto;
	}

	h1 {
		margin-bottom: 1.5rem;
		color: #1a1a2e;
	}

	.user-info {
		background: #f5f5f5;
		padding: 1.5rem;
		border-radius: 8px;
		margin-bottom: 2rem;
	}

	.user-info h2 {
		margin-top: 0;
		margin-bottom: 1rem;
		color: #1a1a2e;
	}

	.user-info p {
		margin: 0.5rem 0;
	}

	.content {
		background: white;
		padding: 1.5rem;
		border: 1px solid #e0e0e0;
		border-radius: 8px;
	}

	.content p {
		margin: 0.5rem 0;
		color: #666;
	}
</style>
