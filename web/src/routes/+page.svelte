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
	const gridPodcasts = $derived(data.popularPodcasts?.podcasts.slice(0, 6) ?? []);
</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Outfit:wght@300;400;500;600&display=swap"
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
	<!-- Ambient Background -->
	<div class="ambient-glow"></div>
	<div class="grain-overlay"></div>

	<!-- Hero Section -->
	<section class="hero">
		<div class="hero-artwork">
			<div class="artwork-frame">
				<div class="artwork-shadow"></div>
				{#if featuredPodcast.cover_url_lg || featuredPodcast.cover_url}
					<img
						src={featuredPodcast.cover_url_lg || featuredPodcast.cover_url}
						alt={featuredPodcast.title}
						class="artwork-image"
					/>
				{:else}
					<div class="artwork-placeholder">
						<div class="placeholder-content">
							<span class="placeholder-author">{featuredPodcast.author ?? 'Featured'}</span>
							<span class="placeholder-presents">presents</span>
							<span class="placeholder-title">{featuredPodcast.title}</span>
						</div>
						<div class="placeholder-texture"></div>
					</div>
				{/if}
				<div class="artwork-reflection"></div>
			</div>

			<!-- Decorative elements -->
			<div class="deco-circle"></div>
			<div class="deco-line"></div>
		</div>

		<div class="hero-content">
			<div class="content-inner">
				<p class="hero-eyebrow">Your podcast companion</p>

				<h1 class="hero-headline">
					<span class="headline-line">track your</span>
					<span class="headline-line headline-accent">favorite</span>
					<span class="headline-line">podcasts.</span>
				</h1>

				<p class="hero-description">
					Discover, follow, and never miss an episode from the shows you love.
				</p>

				<div class="hero-actions">
					{#if data.user}
						<a href="/dashboard" class="btn-primary">
							<span>Go to Dashboard</span>
							<i class="fa-solid fa-arrow-right"></i>
						</a>
					{:else}
						<a href="/signup" class="btn-primary">
							<span>Get Started</span>
							<i class="fa-solid fa-arrow-right"></i>
						</a>
						<a href="/login" class="btn-secondary">Sign in</a>
					{/if}
				</div>

				<div class="platforms">
					<span class="platforms-label">Also available on</span>
					<div class="platform-badges">
						<div class="platform-badge">
							<i class="fa-brands fa-apple"></i>
							<span>iOS</span>
						</div>
						<div class="platform-badge">
							<i class="fa-brands fa-android"></i>
							<span>Android</span>
						</div>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- Popular Podcasts Section -->
	<section class="popular">
		<div class="section-header">
			<div class="header-decoration"></div>
			<h2>Popular right now</h2>
			<div class="header-decoration"></div>
		</div>

		<div class="podcast-carousel">
			{#each gridPodcasts as podcast, i (podcast.id)}
				<article class="podcast-card" style="--i: {i}">
					<div class="card-artwork">
						{#if podcast.cover_url_md || podcast.cover_url}
							<img src={podcast.cover_url_md || podcast.cover_url} alt={podcast.title} />
						{:else}
							<div class="card-placeholder">
								<span>{podcast.title?.charAt(0) ?? '?'}</span>
							</div>
						{/if}
						<div class="card-shine"></div>
						{#if podcast.listen_score}
							<div class="listen-score-badge">{podcast.listen_score}</div>
						{/if}
					</div>
					<div class="card-meta">
						<h3 class="card-title">{podcast.title}</h3>
						{#if podcast.author}
							<span class="card-author">{podcast.author}</span>
						{/if}
					</div>
				</article>
			{:else}
				{#each Array(6) as _, i (i)}
					<article class="podcast-card podcast-card--empty" style="--i: {i}">
						<div class="card-artwork">
							<div class="card-placeholder">
								<i class="fa-solid fa-podcast"></i>
							</div>
						</div>
						<div class="card-meta">
							<h3 class="card-title">Discover</h3>
							<span class="card-author">Coming soon</span>
						</div>
					</article>
				{/each}
			{/each}
		</div>

		<div class="browse-cta">
			<a href="/podcasts" class="browse-link">
				<span>Browse all podcasts</span>
				<i class="fa-solid fa-arrow-right"></i>
			</a>
		</div>
	</section>

	<!-- Features Section -->
	<section class="features">
		<div class="features-grid">
			<div class="feature-card">
				<div class="feature-icon">
					<i class="fa-solid fa-bell"></i>
				</div>
				<h3>Never miss an episode</h3>
				<p>Get notified when new episodes drop from your favorite shows.</p>
			</div>
			<div class="feature-card">
				<div class="feature-icon">
					<i class="fa-solid fa-list"></i>
				</div>
				<h3>Build your library</h3>
				<p>Organize podcasts into collections and track your listening progress.</p>
			</div>
			<div class="feature-card">
				<div class="feature-icon">
					<i class="fa-solid fa-compass"></i>
				</div>
				<h3>Discover new shows</h3>
				<p>Find your next obsession with personalized recommendations.</p>
			</div>
		</div>
	</section>
</div>

<style>
	/* ═══════════════════════════════════════════════════════════════
	   DESIGN TOKENS
	   ═══════════════════════════════════════════════════════════════ */
	.landing {
		--color-bg: #f5f3ee;
		--color-bg-warm: #ebe7df;
		--color-ink: #1a1814;
		--color-ink-muted: #5c574e;
		--color-ink-subtle: #8a847a;
		--color-accent: #c44536;
		--color-accent-warm: #d4654a;
		--color-cream: #faf8f4;

		--font-display: 'Playfair Display', Georgia, serif;
		--font-body: 'Outfit', -apple-system, sans-serif;

		--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
		--ease-out-back: cubic-bezier(0.34, 1.56, 0.64, 1);

		font-family: var(--font-body);
		background: var(--color-bg);
		min-height: 100vh;
		overflow-x: hidden;
		position: relative;
	}

	/* ═══════════════════════════════════════════════════════════════
	   AMBIENT BACKGROUND
	   ═══════════════════════════════════════════════════════════════ */
	.ambient-glow {
		position: fixed;
		top: -30%;
		right: -20%;
		width: 80vw;
		height: 80vw;
		background: radial-gradient(
			ellipse at center,
			rgba(196, 69, 54, 0.08) 0%,
			rgba(196, 69, 54, 0.03) 40%,
			transparent 70%
		);
		pointer-events: none;
		z-index: 0;
	}

	.grain-overlay {
		position: fixed;
		inset: 0;
		background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
		opacity: 0.03;
		pointer-events: none;
		z-index: 1;
	}

	/* ═══════════════════════════════════════════════════════════════
	   HERO SECTION
	   ═══════════════════════════════════════════════════════════════ */
	.hero {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 4rem;
		max-width: 1280px;
		margin: 0 auto;
		padding: 6rem 4rem 8rem;
		position: relative;
		z-index: 2;
		min-height: calc(100vh - 200px);
		align-items: center;
	}

	/* Hero Artwork */
	.hero-artwork {
		position: relative;
		display: flex;
		justify-content: center;
		animation: heroArtworkIn 1s var(--ease-out-expo) both;
	}

	@keyframes heroArtworkIn {
		from {
			opacity: 0;
			transform: translateY(40px) scale(0.95);
		}
		to {
			opacity: 1;
			transform: translateY(0) scale(1);
		}
	}

	.artwork-frame {
		position: relative;
		width: 100%;
		max-width: 420px;
		aspect-ratio: 1;
		border-radius: 12px;
		overflow: hidden;
		transform: rotate(-3deg);
		transition: transform 0.6s var(--ease-out-expo);
	}

	.artwork-frame:hover {
		transform: rotate(0deg) scale(1.02);
	}

	.artwork-shadow {
		position: absolute;
		inset: 0;
		border-radius: inherit;
		box-shadow:
			0 60px 120px -30px rgba(26, 24, 20, 0.35),
			0 30px 60px -20px rgba(196, 69, 54, 0.15);
		z-index: -1;
	}

	.artwork-image {
		width: 100%;
		height: 100%;
		object-fit: cover;
		display: block;
	}

	.artwork-placeholder {
		width: 100%;
		height: 100%;
		background: linear-gradient(
			160deg,
			#8b9ca8 0%,
			#6b7c88 30%,
			#5a6a76 60%,
			#4a5a66 100%
		);
		position: relative;
		overflow: hidden;
	}

	.placeholder-content {
		position: relative;
		z-index: 2;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: flex-start;
		height: 100%;
		padding: 3rem;
	}

	.placeholder-author {
		font-family: var(--font-display);
		font-size: clamp(1.75rem, 4vw, 2.5rem);
		color: var(--color-ink);
		font-weight: 500;
		text-transform: uppercase;
		letter-spacing: 0.04em;
		line-height: 1;
	}

	.placeholder-presents {
		font-family: var(--font-display);
		font-style: italic;
		font-size: clamp(0.875rem, 2vw, 1rem);
		color: rgba(26, 24, 20, 0.6);
		margin: 0.75rem 0;
		text-transform: uppercase;
		letter-spacing: 0.25em;
	}

	.placeholder-title {
		font-family: var(--font-display);
		font-size: clamp(2.5rem, 7vw, 4.5rem);
		color: var(--color-accent);
		font-weight: 500;
		text-transform: uppercase;
		letter-spacing: -0.02em;
		line-height: 0.85;
		opacity: 0.9;
	}

	.placeholder-texture {
		position: absolute;
		inset: 0;
		background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
		opacity: 0.12;
		mix-blend-mode: overlay;
		z-index: 1;
	}

	.artwork-reflection {
		position: absolute;
		inset: 0;
		background: linear-gradient(
			135deg,
			rgba(255, 255, 255, 0.15) 0%,
			transparent 50%
		);
		pointer-events: none;
	}

	/* Decorative elements */
	.deco-circle {
		position: absolute;
		bottom: -30px;
		right: -30px;
		width: 120px;
		height: 120px;
		border: 2px solid var(--color-accent);
		border-radius: 50%;
		opacity: 0.2;
		animation: decoFade 1s 0.3s var(--ease-out-expo) both;
	}

	.deco-line {
		position: absolute;
		top: 50%;
		left: -60px;
		width: 40px;
		height: 2px;
		background: var(--color-ink);
		opacity: 0.15;
		animation: decoFade 1s 0.4s var(--ease-out-expo) both;
	}

	@keyframes decoFade {
		from { opacity: 0; }
		to { opacity: 0.2; }
	}

	/* Hero Content */
	.hero-content {
		position: relative;
	}

	.content-inner {
		max-width: 500px;
	}

	.hero-eyebrow {
		font-size: 0.75rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.2em;
		color: var(--color-accent);
		margin: 0 0 1.5rem;
		opacity: 0;
		animation: contentIn 0.8s 0.2s var(--ease-out-expo) forwards;
	}

	.hero-headline {
		font-family: var(--font-display);
		font-size: clamp(3rem, 6vw, 4.5rem);
		font-weight: 500;
		line-height: 1.05;
		color: var(--color-ink);
		margin: 0 0 1.5rem;
		letter-spacing: -0.02em;
	}

	.headline-line {
		display: block;
		opacity: 0;
		animation: headlineIn 0.8s var(--ease-out-expo) forwards;
	}

	.headline-line:nth-child(1) { animation-delay: 0.3s; }
	.headline-line:nth-child(2) { animation-delay: 0.4s; }
	.headline-line:nth-child(3) { animation-delay: 0.5s; }

	@keyframes headlineIn {
		from {
			opacity: 0;
			transform: translateY(30px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.headline-accent {
		font-style: italic;
		color: var(--color-accent);
	}

	.hero-description {
		font-size: 1.125rem;
		line-height: 1.6;
		color: var(--color-ink-muted);
		margin: 0 0 2.5rem;
		max-width: 400px;
		opacity: 0;
		animation: contentIn 0.8s 0.6s var(--ease-out-expo) forwards;
	}

	@keyframes contentIn {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	/* Hero Actions */
	.hero-actions {
		display: flex;
		gap: 1rem;
		margin-bottom: 3rem;
		opacity: 0;
		animation: contentIn 0.8s 0.7s var(--ease-out-expo) forwards;
	}

	.btn-primary {
		display: inline-flex;
		align-items: center;
		gap: 0.75rem;
		background: var(--color-ink);
		color: var(--color-cream);
		padding: 1rem 2rem;
		font-family: var(--font-body);
		font-size: 0.9375rem;
		font-weight: 500;
		text-decoration: none;
		border-radius: 100px;
		transition: all 0.4s var(--ease-out-expo);
		box-shadow: 0 4px 20px rgba(26, 24, 20, 0.2);
	}

	.btn-primary:hover {
		background: var(--color-accent);
		transform: translateY(-2px);
		box-shadow: 0 8px 30px rgba(196, 69, 54, 0.3);
	}

	.btn-primary i {
		font-size: 0.75rem;
		transition: transform 0.3s var(--ease-out-expo);
	}

	.btn-primary:hover i {
		transform: translateX(4px);
	}

	.btn-secondary {
		display: inline-flex;
		align-items: center;
		padding: 1rem 1.5rem;
		font-family: var(--font-body);
		font-size: 0.9375rem;
		font-weight: 500;
		color: var(--color-ink);
		text-decoration: none;
		border-radius: 100px;
		transition: all 0.3s var(--ease-out-expo);
	}

	.btn-secondary:hover {
		color: var(--color-accent);
	}

	/* Platforms */
	.platforms {
		display: flex;
		align-items: center;
		gap: 1.25rem;
		opacity: 0;
		animation: contentIn 0.8s 0.8s var(--ease-out-expo) forwards;
	}

	.platforms-label {
		font-size: 0.8125rem;
		color: var(--color-ink-subtle);
		letter-spacing: 0.02em;
	}

	.platform-badges {
		display: flex;
		gap: 0.5rem;
	}

	.platform-badge {
		display: flex;
		align-items: center;
		gap: 0.4rem;
		padding: 0.5rem 0.875rem;
		background: var(--color-cream);
		border-radius: 100px;
		font-size: 0.75rem;
		font-weight: 500;
		color: var(--color-ink);
		box-shadow: 0 2px 8px rgba(26, 24, 20, 0.06);
		transition: all 0.3s var(--ease-out-expo);
	}

	.platform-badge:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(26, 24, 20, 0.1);
	}

	.platform-badge i {
		font-size: 1rem;
	}

	/* ═══════════════════════════════════════════════════════════════
	   POPULAR SECTION
	   ═══════════════════════════════════════════════════════════════ */
	.popular {
		position: relative;
		z-index: 2;
		max-width: 1280px;
		margin: 0 auto;
		padding: 0 4rem 6rem;
	}

	.section-header {
		display: flex;
		align-items: center;
		gap: 2rem;
		margin-bottom: 3rem;
	}

	.section-header h2 {
		font-family: var(--font-display);
		font-size: 1.125rem;
		font-weight: 400;
		font-style: italic;
		color: var(--color-ink);
		white-space: nowrap;
		margin: 0;
	}

	.header-decoration {
		flex: 1;
		height: 1px;
		background: linear-gradient(
			90deg,
			transparent 0%,
			var(--color-ink) 50%,
			transparent 100%
		);
		opacity: 0.12;
	}

	/* Podcast Carousel */
	.podcast-carousel {
		display: grid;
		grid-template-columns: repeat(6, 1fr);
		gap: 1.5rem;
	}

	.podcast-card {
		min-width: 0;
		opacity: 0;
		animation: cardIn 0.6s var(--ease-out-expo) forwards;
		animation-delay: calc(0.1s + var(--i) * 0.08s);
	}

	@keyframes cardIn {
		from {
			opacity: 0;
			transform: translateY(30px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.card-artwork {
		position: relative;
		aspect-ratio: 1;
		border-radius: 8px;
		overflow: hidden;
		background: var(--color-bg-warm);
		margin-bottom: 0.875rem;
		box-shadow: 0 8px 30px rgba(26, 24, 20, 0.08);
		transition: all 0.4s var(--ease-out-expo);
	}

	.podcast-card:hover .card-artwork {
		transform: translateY(-6px) scale(1.02);
		box-shadow: 0 20px 50px rgba(26, 24, 20, 0.15);
	}

	.card-artwork img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		transition: transform 0.6s var(--ease-out-expo);
	}

	.podcast-card:hover .card-artwork img {
		transform: scale(1.05);
	}

	.card-shine {
		position: absolute;
		inset: 0;
		background: linear-gradient(
			135deg,
			rgba(255, 255, 255, 0.2) 0%,
			transparent 60%
		);
		opacity: 0;
		transition: opacity 0.4s var(--ease-out-expo);
	}

	.podcast-card:hover .card-shine {
		opacity: 1;
	}

	.listen-score-badge {
		position: absolute;
		top: 0.5rem;
		right: 0.5rem;
		background: var(--color-accent);
		color: var(--color-cream);
		font-size: 0.6875rem;
		font-weight: 600;
		padding: 0.25rem 0.5rem;
		border-radius: 100px;
		box-shadow: 0 2px 8px rgba(196, 69, 54, 0.3);
		z-index: 2;
	}

	.card-placeholder {
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		background: linear-gradient(135deg, var(--color-bg-warm) 0%, #ddd9cf 100%);
	}

	.card-placeholder span,
	.card-placeholder i {
		font-family: var(--font-display);
		font-size: 1.75rem;
		color: var(--color-ink);
		opacity: 0.2;
	}

	.card-meta {
		padding: 0 0.25rem;
	}

	.card-title {
		font-family: var(--font-body);
		font-size: 0.875rem;
		font-weight: 500;
		color: var(--color-ink);
		margin: 0 0 0.25rem;
		line-height: 1.3;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.card-author {
		font-size: 0.75rem;
		color: var(--color-ink-subtle);
	}

	.podcast-card--empty {
		opacity: 0.5;
	}

	/* Browse CTA */
	.browse-cta {
		display: flex;
		justify-content: center;
		margin-top: 3rem;
	}

	.browse-link {
		display: inline-flex;
		align-items: center;
		gap: 0.75rem;
		font-size: 0.9375rem;
		font-weight: 500;
		color: var(--color-ink);
		text-decoration: none;
		padding: 0.75rem 0;
		border-bottom: 1px solid transparent;
		transition: all 0.3s var(--ease-out-expo);
	}

	.browse-link:hover {
		color: var(--color-accent);
		border-color: var(--color-accent);
	}

	.browse-link i {
		font-size: 0.75rem;
		transition: transform 0.3s var(--ease-out-expo);
	}

	.browse-link:hover i {
		transform: translateX(4px);
	}

	/* ═══════════════════════════════════════════════════════════════
	   FEATURES SECTION
	   ═══════════════════════════════════════════════════════════════ */
	.features {
		position: relative;
		z-index: 2;
		background: var(--color-ink);
		padding: 6rem 4rem;
		margin-top: 4rem;
	}

	.features-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 3rem;
		max-width: 1280px;
		margin: 0 auto;
	}

	.feature-card {
		text-align: center;
		padding: 2rem;
	}

	.feature-icon {
		width: 56px;
		height: 56px;
		margin: 0 auto 1.5rem;
		display: flex;
		align-items: center;
		justify-content: center;
		background: rgba(255, 255, 255, 0.08);
		border-radius: 16px;
		transition: all 0.4s var(--ease-out-expo);
	}

	.feature-card:hover .feature-icon {
		background: var(--color-accent);
		transform: translateY(-4px);
	}

	.feature-icon i {
		font-size: 1.25rem;
		color: var(--color-cream);
	}

	.feature-card h3 {
		font-family: var(--font-display);
		font-size: 1.25rem;
		font-weight: 500;
		color: var(--color-cream);
		margin: 0 0 0.75rem;
	}

	.feature-card p {
		font-size: 0.9375rem;
		line-height: 1.6;
		color: rgba(250, 248, 244, 0.6);
		margin: 0;
	}

	/* ═══════════════════════════════════════════════════════════════
	   RESPONSIVE
	   ═══════════════════════════════════════════════════════════════ */
	@media (max-width: 1100px) {
		.podcast-carousel {
			grid-template-columns: repeat(4, 1fr);
		}

		.podcast-card:nth-child(n+5) {
			display: none;
		}
	}

	@media (max-width: 900px) {
		.hero {
			grid-template-columns: 1fr;
			gap: 3rem;
			padding: 4rem 2rem 6rem;
			text-align: center;
		}

		.hero-artwork {
			order: -1;
		}

		.artwork-frame {
			max-width: 320px;
			transform: rotate(0deg);
		}

		.content-inner {
			max-width: 100%;
		}

		.hero-description {
			max-width: 100%;
		}

		.hero-actions {
			justify-content: center;
		}

		.platforms {
			justify-content: center;
		}

		.deco-circle,
		.deco-line {
			display: none;
		}

		.features-grid {
			grid-template-columns: 1fr;
			gap: 2rem;
		}
	}

	@media (max-width: 768px) {
		.hero {
			padding: 3rem 1.5rem 4rem;
		}

		.hero-headline {
			font-size: 2.5rem;
		}

		.popular {
			padding: 0 1.5rem 4rem;
		}

		.podcast-carousel {
			grid-template-columns: repeat(3, 1fr);
			gap: 1rem;
		}

		.podcast-card:nth-child(n+4) {
			display: none;
		}

		.features {
			padding: 4rem 1.5rem;
		}

		.feature-card {
			padding: 1.5rem;
		}
	}

	@media (max-width: 480px) {
		.artwork-frame {
			max-width: 260px;
		}

		.hero-actions {
			flex-direction: column;
			align-items: center;
		}

		.podcast-carousel {
			grid-template-columns: repeat(2, 1fr);
		}

		.podcast-card:nth-child(n+3) {
			display: none;
		}

		.platforms {
			flex-direction: column;
			gap: 0.75rem;
		}
	}
</style>
