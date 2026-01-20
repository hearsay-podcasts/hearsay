<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	// Featured podcast for hero (use first from API or fallback)
	const featuredPodcast = $derived(
		data.popularPodcasts?.podcasts[0] ?? {
			title: 'Burn Order',
			author: 'Rachel Maddow',
			cover_url: null
		}
	);

	// Remaining podcasts for the grid
	const gridPodcasts = $derived(data.popularPodcasts?.podcasts.slice(0, 4) ?? []);
</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&display=swap"
		rel="stylesheet"
	/>
	<link
		rel="stylesheet"
		href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
		integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA=="
		crossorigin="anonymous"
		referrerpolicy="no-referrer"
	/>
	<title>hearsay — track your favorite podcasts</title>
</svelte:head>

<div class="landing">
	<!-- Hero Section -->
	<section class="hero">
		<div class="hero-visual">
			<div class="featured-cover">
				{#if featuredPodcast.cover_url}
					<img src={featuredPodcast.cover_url} alt={featuredPodcast.title} />
				{:else}
					<div class="cover-placeholder">
						<span class="placeholder-author">{featuredPodcast.author ?? 'Featured'}</span>
						<span class="placeholder-presents">presents</span>
						<span class="placeholder-title">{featuredPodcast.title}</span>
					</div>
				{/if}
			</div>
			<div class="visual-noise"></div>
		</div>

		<div class="hero-content">
			<h1 class="tagline">
				track your favorite<br />
				<span class="tagline-accent">podcasts.</span>
			</h1>

			<div class="hero-cta">
				{#if data.user}
					<a href="/dashboard" class="btn-primary">Go to Dashboard</a>
				{:else}
					<a href="/signup" class="btn-primary">Sign up</a>
				{/if}
			</div>

			<div class="platforms">
				<span class="platforms-label">Also available on</span>
				<div class="platform-icons">
					<i class="fa-brands fa-apple platform-icon"></i>
					<i class="fa-brands fa-android platform-icon"></i>
				</div>
			</div>
		</div>
	</section>

	<!-- Popular Podcasts Section -->
	<section class="popular">
		<div class="popular-header">
			<h2>Popular podcasts</h2>
			<div class="header-line"></div>
		</div>

		<div class="podcast-grid">
			{#each gridPodcasts as podcast, i (podcast.id)}
				<article class="podcast-card" style="--delay: {i * 0.1}s">
					<div class="card-cover">
						{#if podcast.cover_url}
							<img src={podcast.cover_url} alt={podcast.title} />
						{:else}
							<div class="card-placeholder">
								<span>{podcast.title.charAt(0)}</span>
							</div>
						{/if}
					</div>
					<div class="card-info">
						<h3>{podcast.title}</h3>
						{#if podcast.author}
							<span class="card-author">{podcast.author}</span>
						{/if}
					</div>
				</article>
			{:else}
				{#each Array(4) as _, i (i)}
					<article class="podcast-card podcast-card-empty" style="--delay: {i * 0.1}s">
						<div class="card-cover">
							<div class="card-placeholder">
								<span>?</span>
							</div>
						</div>
						<div class="card-info">
							<h3>Coming soon</h3>
							<span class="card-author">Add podcasts to see them here</span>
						</div>
					</article>
				{/each}
			{/each}
		</div>
	</section>
</div>

<style>
	/* Landing page scoped styles */
	.landing {
		font-family: 'DM Sans', sans-serif;
		min-height: calc(100vh - 60px);
		background: linear-gradient(
			180deg,
			#f8f7f4 0%,
			#f0efe9 40%,
			#e8e6de 100%
		);
		overflow-x: hidden;
	}

	/* Hero Section */
	.hero {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 2rem;
		max-width: 1200px;
		margin: 0 auto;
		padding: 4rem 3rem 6rem;
		align-items: center;
	}

	.hero-visual {
		position: relative;
	}

	.featured-cover {
		position: relative;
		width: 100%;
		aspect-ratio: 1;
		max-width: 480px;
		border-radius: 8px;
		overflow: hidden;
		box-shadow:
			0 50px 100px -20px rgba(26, 26, 46, 0.25),
			0 30px 60px -30px rgba(26, 26, 46, 0.3);
		transform: rotate(-2deg);
		transition: transform 0.4s cubic-bezier(0.23, 1, 0.32, 1);
	}

	.featured-cover:hover {
		transform: rotate(0deg) scale(1.02);
	}

	.featured-cover img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.cover-placeholder {
		width: 100%;
		height: 100%;
		background: linear-gradient(
			145deg,
			#8b9ca8 0%,
			#6b7c88 50%,
			#4a5a66 100%
		);
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: flex-start;
		padding: 2.5rem;
		position: relative;
		overflow: hidden;
	}

	.cover-placeholder::before {
		content: '';
		position: absolute;
		inset: 0;
		background: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%' height='100%' filter='url(%23noise)'/%3E%3C/svg%3E");
		opacity: 0.15;
		mix-blend-mode: overlay;
	}

	.placeholder-author {
		font-family: 'Instrument Serif', Georgia, serif;
		font-size: clamp(1.5rem, 4vw, 2.5rem);
		color: #1a1a2e;
		font-weight: 400;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		line-height: 1.1;
	}

	.placeholder-presents {
		font-family: 'Instrument Serif', Georgia, serif;
		font-style: italic;
		font-size: clamp(0.9rem, 2vw, 1.1rem);
		color: rgba(26, 26, 46, 0.7);
		margin: 0.5rem 0;
		text-transform: uppercase;
		letter-spacing: 0.2em;
	}

	.placeholder-title {
		font-family: 'Instrument Serif', Georgia, serif;
		font-size: clamp(2rem, 6vw, 4rem);
		color: #c44536;
		font-weight: 400;
		text-transform: uppercase;
		letter-spacing: -0.02em;
		line-height: 0.9;
		opacity: 0.85;
	}

	.visual-noise {
		position: absolute;
		inset: 0;
		pointer-events: none;
		background: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7'/%3E%3C/filter%3E%3Crect width='100%' height='100%' filter='url(%23n)'/%3E%3C/svg%3E");
		opacity: 0.03;
	}

	/* Hero Content */
	.hero-content {
		padding-left: 2rem;
	}

	.tagline {
		font-family: 'Instrument Serif', Georgia, serif;
		font-size: clamp(2.5rem, 5vw, 4rem);
		font-weight: 400;
		line-height: 1.1;
		color: #1a1a2e;
		margin: 0 0 2.5rem;
		letter-spacing: -0.02em;
	}

	.tagline-accent {
		font-style: italic;
		color: #1a1a2e;
	}

	.hero-cta {
		margin-bottom: 3rem;
	}

	.btn-primary {
		display: inline-block;
		background: #1a1a2e;
		color: #f8f7f4;
		padding: 1rem 2.5rem;
		font-family: 'DM Sans', sans-serif;
		font-size: 1rem;
		font-weight: 500;
		text-decoration: none;
		border-radius: 4px;
		transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
		box-shadow: 0 4px 14px rgba(26, 26, 46, 0.25);
	}

	.btn-primary:hover {
		background: #2d2d4a;
		transform: translateY(-2px);
		box-shadow: 0 6px 20px rgba(26, 26, 46, 0.35);
	}

	/* Platforms */
	.platforms {
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	.platforms-label {
		font-size: 0.875rem;
		color: #666;
		letter-spacing: 0.02em;
	}

	.platform-icons {
		display: flex;
		gap: 0.75rem;
	}

	.platform-icon {
		font-size: 1.375rem;
		color: #1a1a2e;
		opacity: 0.7;
		transition: opacity 0.2s;
	}

	.platform-icon:hover {
		opacity: 1;
	}

	/* Popular Section */
	.popular {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 3rem 6rem;
	}

	.popular-header {
		display: flex;
		align-items: center;
		gap: 2rem;
		margin-bottom: 2.5rem;
	}

	.popular-header h2 {
		font-family: 'Instrument Serif', Georgia, serif;
		font-size: 1.25rem;
		font-weight: 400;
		font-style: italic;
		color: #1a1a2e;
		white-space: nowrap;
		margin: 0;
	}

	.header-line {
		flex: 1;
		height: 1px;
		background: linear-gradient(90deg, #1a1a2e 0%, transparent 100%);
		opacity: 0.2;
	}

	/* Podcast Grid */
	.podcast-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 1.5rem;
	}

	.podcast-card {
		opacity: 0;
		animation: fadeSlideUp 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards;
		animation-delay: var(--delay, 0s);
	}

	@keyframes fadeSlideUp {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.card-cover {
		aspect-ratio: 1;
		border-radius: 6px;
		overflow: hidden;
		margin-bottom: 0.875rem;
		background: #e0ded6;
		box-shadow: 0 8px 30px rgba(26, 26, 46, 0.08);
		transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
	}

	.podcast-card:hover .card-cover {
		transform: translateY(-4px);
		box-shadow: 0 12px 40px rgba(26, 26, 46, 0.15);
	}

	.card-cover img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.card-placeholder {
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		background: linear-gradient(135deg, #d4d2ca 0%, #c4c2ba 100%);
	}

	.card-placeholder span {
		font-family: 'Instrument Serif', Georgia, serif;
		font-size: 2rem;
		color: #1a1a2e;
		opacity: 0.3;
	}

	.card-info h3 {
		font-family: 'DM Sans', sans-serif;
		font-size: 0.9375rem;
		font-weight: 500;
		color: #1a1a2e;
		margin: 0 0 0.25rem;
		line-height: 1.3;
	}

	.card-author {
		font-size: 0.8125rem;
		color: #666;
	}

	.podcast-card-empty {
		opacity: 0.6;
	}

	.podcast-card-empty .card-placeholder span {
		opacity: 0.2;
	}

	/* Responsive */
	@media (max-width: 1024px) {
		.hero {
			grid-template-columns: 1fr;
			text-align: center;
			padding: 3rem 2rem 4rem;
		}

		.hero-visual {
			order: -1;
			display: flex;
			justify-content: center;
		}

		.featured-cover {
			max-width: 350px;
			transform: rotate(0deg);
		}

		.hero-content {
			padding-left: 0;
		}

		.platforms {
			justify-content: center;
		}

		.podcast-grid {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	@media (max-width: 640px) {
		.hero {
			padding: 2rem 1.5rem 3rem;
		}

		.featured-cover {
			max-width: 280px;
		}

		.tagline {
			font-size: 2rem;
		}

		.popular {
			padding: 0 1.5rem 4rem;
		}

		.podcast-grid {
			grid-template-columns: repeat(2, 1fr);
			gap: 1rem;
		}
	}
</style>
