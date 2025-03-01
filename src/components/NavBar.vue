<script setup>
import { RouterLink } from "vue-router";
import Github from "./icons/Github.vue";
import Instagram from "./icons/Instagram.vue";
import Linkedin from "./icons/Linkedin.vue";
import Telegram from "./icons/Telegram.vue";
import Email from "./icons/Email.vue";

const websiteLinks = [
	{ name: "Home", path: "/" },
	{ name: "Blogs", path: "/blogs" },
	{ name: "Gallery", path: "/gallery" },
	{ name: "About", path: "/about" },
];

const socialLinks = [
	{ icon: Github, href: "https://github.com/krantheman" },
	{ icon: Linkedin, href: "https://www.linkedin.com/in/akash-tom/" },
	{ icon: Instagram, href: "https://www.instagram.com/monsieur_le_tom/" },
	{ icon: Telegram, href: "https://t.me/akash_tom" },
	{ icon: Email, href: "mailto:me@akashtom.com" },
];
</script>

<template>
	<header>
		<nav class="h-12 flex space-x-8 items-end">
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
			<div class="mx-auto hidden sm:block" />
			<a
				v-for="link in socialLinks"
				:href="link.href"
				target="_blank"
				rel="noopener"
				class="hidden sm:block"
			>
				<component
					:is="link.icon"
					class="h-4.5 w-4.5 fill-gray-300 hover:fill-sky-300"
				/>
			</a>
		</nav>
	</header>
</template>
