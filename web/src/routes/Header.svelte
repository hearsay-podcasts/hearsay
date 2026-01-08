<script lang="ts">
	import { resolve } from '$app/paths';
</script>

<header class="flex justify-between items-center px-6 py-4 bg-white">
	<!-- Logo/Brand -->
	<div>
		<a href={resolve('/')} class="text-2xl font-bold text-gray-900">hearsay</a>
	</div>

	<!-- Navigation -->
	<nav class="flex items-center gap-6">
		<button class="text-sm font-medium text-gray-700 hover:text-gray-900 transition uppercase tracking-wide">Podcasts</button>
		<button class="text-sm font-medium text-gray-700 hover:text-gray-900 transition uppercase tracking-wide">Sign In</button>
		<button class="bg-black text-white px-4 py-2 rounded text-sm font-semibold hover:bg-gray-800 transition uppercase tracking-wide">Create Account</button>
		<button aria-label="Search" class="text-gray-600 hover:text-gray-900 transition">
			<i class="fas fa-search text-xl"></i>
		</button>
	</nav>
</header>
