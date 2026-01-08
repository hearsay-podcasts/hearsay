<script lang="ts">
	import PodcastCard from './PodcastCard.svelte';

	const podcasts = [
		{ id: 1, fallback: 'Pod' },
		{ id: 2, fallback: 'Cast' },
		{ id: 3, fallback: 'Show' },
		{ id: 4, fallback: 'Audio' }
	];
</script>

<section class="px-6 py-24 md:px-12 md:py-32">
	<div class="mx-auto max-w-7xl">
		<!-- Section header -->
		<div class="mb-16 flex items-end justify-between">
			<h2 class="font-display text-4xl font-semibold tracking-tight text-[#1A1A1A] md:text-5xl lg:text-6xl">
				Popular<br />shows
			</h2>
			<div class="hidden md:block">
				<p class="font-mono text-xs uppercase tracking-[0.15em] text-[#6B6B6B]">
					Trending now
				</p>
			</div>
		</div>

		<!-- Grid with staggered animation -->
		<div class="podcast-grid grid grid-cols-2 gap-4 md:gap-6 lg:grid-cols-4">
			{#each podcasts as podcast, i (podcast.id)}
				<div style="animation-delay: {i * 100}ms">
					<PodcastCard fallbackText={podcast.fallback} />
				</div>
			{/each}
		</div>

		<!-- Bottom accent -->
		<div class="mt-16 flex justify-center">
			<div class="h-0.5 w-24 bg-[#FF6B4A]"></div>
		</div>
	</div>
</section>

<style>
	@keyframes slideUp {
		from {
			opacity: 0;
			transform: translateY(30px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.podcast-grid > div {
		animation: slideUp 0.6s ease-out both;
	}
</style>
