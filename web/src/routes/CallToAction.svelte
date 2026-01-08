<section class="px-6 py-24 md:px-12 md:py-32 lg:py-40">
	<div class="mx-auto max-w-5xl">
		<!-- Main heading with asymmetric layout -->
		<div class="mb-16 md:mb-20">
			<h1 class="font-display text-6xl font-semibold leading-[0.9] tracking-tight text-[#1A1A1A] md:text-8xl lg:text-9xl">
				Track your<br />
				<span class="italic text-[#FF6B4A]">favorite</span><br />
				podcasts.
			</h1>
		</div>

		<!-- CTA and platform info in horizontal layout -->
		<div class="flex flex-col items-start gap-12 md:flex-row md:items-center md:justify-between">
			<!-- Left: CTA -->
			<div>
				<button
					class="group relative overflow-hidden bg-[#1A1A1A] px-12 py-5 font-medium text-[#FDFBF7] transition-all duration-300 hover:bg-[#FF6B4A]"
				>
					<span class="relative z-10">Sign up</span>
					<div class="absolute inset-0 -translate-x-full bg-[#FF6B4A] transition-transform duration-300 group-hover:translate-x-0"></div>
				</button>
			</div>

			<!-- Right: Platform availability -->
			<div class="flex items-center gap-6">
				<span class="font-mono text-xs uppercase tracking-[0.15em] text-[#6B6B6B]">
					Also on
				</span>
				<div class="flex gap-4">
					<div class="flex h-12 w-12 items-center justify-center rounded-full border border-[#1A1A1A]/10 transition-colors hover:border-[#FF6B4A]">
						<i class="fab fa-apple text-2xl text-[#1A1A1A]"></i>
					</div>
					<div class="flex h-12 w-12 items-center justify-center rounded-full border border-[#1A1A1A]/10 transition-colors hover:border-[#FF6B4A]">
						<i class="fab fa-android text-2xl text-[#1A1A1A]"></i>
					</div>
				</div>
			</div>
		</div>
	</div>
</section>

<style>
	button span {
		position: relative;
		z-index: 10;
	}
</style>
