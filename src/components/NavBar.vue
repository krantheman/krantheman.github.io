<script setup>
import { RouterLink, RouterView, useRoute } from "vue-router";

const route = useRoute();

const links = [
	{ name: "Home", path: "/" },
	{ name: "Blogs", path: "/blogs" },
	{ name: "Gallery", path: "/gallery" },
	{ name: "About", path: "/about" },
];
</script>

<template>
	<header>
		<nav class="flex justify-between">
			<RouterLink
				v-for="link in links"
				:to="link.path"
				class="hover:text-sky-200"
				:class="{ 'text-sky-200': route.name === link.name }"
			>
				{{ link.name }}
			</RouterLink>
		</nav>
	</header>
</template>
