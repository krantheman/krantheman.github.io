<script setup>
import { RouterLink } from "vue-router";
import Socials from "@/components/Socials.vue";

const websiteLinks = [
	{ name: "Home", path: "/" },
	{ name: "Gallery", path: "/gallery" },
	{ name: "Blog", path: "/blog" },
	{ name: "Projects", path: "/projects" },
];
</script>

<template>
	<header class="sticky top-0 bg-[rgb(20,20,20)] z-20 py-4">
		<nav class="flex items-center">
			<div class="flex w-full sm:w-auto justify-between space-x-8">
				<RouterLink
					v-for="link in websiteLinks"
					:to="link.path"
					class="font-medium"
					:class="{
						'!no-underline': $route.path.split('/')[1] !== link.path.slice(1),
					}"
				>
					{{ link.name }}
				</RouterLink>
			</div>
			<div class="sm:flex items-center space-x-8 ml-auto hidden">
				<Socials />
			</div>
		</nav>
	</header>
</template>
