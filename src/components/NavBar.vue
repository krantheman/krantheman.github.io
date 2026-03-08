<script setup>
const websiteLinks = [
	{ name: "Home", path: "/" },
	{ name: "Places", path: "/places" },
	{ name: "Journal", path: "/journal" },
	{ name: "Work", path: "/work" },
];
</script>

<template>
	<header class="sticky top-0 bg-body z-20">
		<nav class="flex items-center py-4">
			<div class="flex w-full max-sm:justify-between sm:space-x-12">
				<router-link
					v-for="link in websiteLinks"
					:to="link.path"
					class="font-medium"
					:class="{
						'no-underline!': $route.path.split('/')[1] !== link.path.slice(1),
					}"
				>
					{{ link.name }}
				</router-link>
			</div>
		</nav>
	</header>
</template>
