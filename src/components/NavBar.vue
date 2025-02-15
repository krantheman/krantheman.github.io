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
		<nav class="h-16 flex space-x-8 items-center">
			<RouterLink
				v-for="link in websiteLinks"
				:to="link.path"
				class="hover:text-sky-200 font-medium text-lg"
				:class="{
					'text-sky-200': $route.path.split('/')[1] === link.path.slice(1),
				}"
			>
				{{ link.name }}
			</RouterLink>
			<div class="mx-auto" />
			<a
				v-for="link in socialLinks"
				:href="link.href"
				target="_blank"
				rel="noopener"
			>
				<component
					:is="link.icon"
					class="h-5 w-5 fill-gray-200 hover:fill-sky-200"
				/>
			</a>
		</nav>
	</header>
</template>
