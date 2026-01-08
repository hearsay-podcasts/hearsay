<script lang="ts">
	interface Props {
		title?: string;
		fallbackText?: string;
	}

	let { title, fallbackText = 'blah' }: Props = $props();
</script>

<article class="podcast-card group relative aspect-square overflow-hidden border border-[#1A1A1A]/5 bg-linear-to-br from-[#F5F5F0] to-[#E8E8E0] transition-all duration-500 hover:border-[#FF6B4A]/30 hover:shadow-2xl hover:shadow-[#FF6B4A]/10">
	<!-- Decorative corner accent -->
	<div class="absolute right-0 top-0 h-16 w-16 translate-x-12 -translate-y-12 rounded-full bg-[#FF6B4A] opacity-0 blur-2xl transition-all duration-500 group-hover:translate-x-0 group-hover:translate-y-0 group-hover:opacity-20"></div>

	<!-- Content -->
	<div class="relative flex h-full w-full flex-col items-center justify-center p-8">
		<span class="font-display text-2xl font-semibold text-[#1A1A1A]/20 transition-all duration-500 group-hover:text-[#FF6B4A]/40">
			{fallbackText}
		</span>
	</div>

	<!-- Hover state indicator -->
	<div class="absolute bottom-0 left-0 h-1 w-0 bg-[#FF6B4A] transition-all duration-500 group-hover:w-full"></div>
</article>

<style>
	.podcast-card {
		transform: translateY(0);
	}

	.podcast-card:hover {
		transform: translateY(-4px);
	}
</style>
