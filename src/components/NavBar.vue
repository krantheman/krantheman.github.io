<script setup>
import { RouterLink } from "vue-router";
import Github from "@/components/icons/Github.vue";
import Instagram from "@/components/icons/Instagram.vue";
import Linkedin from "@/components/icons/Linkedin.vue";
import Telegram from "@/components/icons/Telegram.vue";
import Email from "@/components/icons/Email.vue";

const websiteLinks = [
	{ name: "Home", path: "/" },
	{ name: "Gallery", path: "/gallery" },
	{ name: "Blog", path: "/blog" },
	{ name: "Projects", path: "/projects" },
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
		<nav class="h-12 flex items-end">
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
				<a
					v-for="link in socialLinks"
					:href="link.href"
					target="_blank"
					rel="noopener"
					class="hidden sm:block"
				>
					<component
						:is="link.icon"
						class="h-4.5 w-4.5 fill-gray-200 hover:fill-sky-200 active:fill-sky-200"
					/>
				</a>
			</div>
		</nav>
	</header>
</template>
