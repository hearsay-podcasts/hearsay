<script lang="ts">
	import Hero from './Hero.svelte';
	import CallToAction from './CallToAction.svelte';
	import PopularPodcasts from './PopularPodcasts.svelte';
</script>

<svelte:head>
	<title>Hearsay - Track Your Favorite Podcasts</title>
	<meta name="description" content="Track and manage your favorite podcasts in one place" />
</svelte:head>

<main class="w-full">
	<Hero />
	<CallToAction />
	<PopularPodcasts />
</main>
