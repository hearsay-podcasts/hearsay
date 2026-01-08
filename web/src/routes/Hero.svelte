<div class="relative w-full overflow-hidden bg-[#1A1A1A] px-6 py-24 md:px-12 md:py-32 lg:py-40">
	<!-- Background decorative element -->
	<div class="absolute right-0 top-0 h-full w-1/2 opacity-5">
		<div class="h-full w-full bg-linear-to-br from-[#FF6B4A] to-transparent"></div>
	</div>

	<!-- Content -->
	<div class="relative mx-auto max-w-7xl">
		<div class="flex flex-col items-start gap-8 md:flex-row md:items-end md:justify-between">
			<!-- Left: Featured podcast -->
			<div class="flex-1">
				<p class="mb-4 font-mono text-xs uppercase tracking-[0.2em] text-[#FF6B4A] md:text-sm">
					Featured
				</p>
				<h2 class="mb-3 font-display text-5xl font-semibold leading-[0.95] tracking-tight text-[#FDFBF7] md:text-7xl lg:text-8xl">
					BURN<br />ORDER
				</h2>
				<p class="font-display text-lg italic text-[#6B6B6B] md:text-xl">
					Rachel Maddow Presents
				</p>
			</div>

			<!-- Right: Decorative element -->
			<div class="hidden md:block">
				<div class="h-32 w-32 rounded-full border border-[#FF6B4A]/20"></div>
			</div>
		</div>
	</div>
</div>

<style>
	@keyframes fadeInUp {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	div {
		animation: fadeInUp 0.8s ease-out;
	}
</style>
