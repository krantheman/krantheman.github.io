<script setup>
import Github from "@/components/icons/Github.vue";
import Instagram from "@/components/icons/Instagram.vue";
import Linkedin from "@/components/icons/Linkedin.vue";
import Telegram from "@/components/icons/Telegram.vue";
import Email from "@/components/icons/Email.vue";

const socialLinks = [
	{ title: "GitHub", icon: Github, href: "https://github.com/krantheman" },
	{
		title: "Instagram",
		icon: Instagram,
		href: "https://www.instagram.com/monsieur_le_tom/",
	},
	{
		title: "LinkedIn",
		icon: Linkedin,
		href: "https://www.linkedin.com/in/akash-tom/",
	},
	{ title: "Telegram", icon: Telegram, href: "https://t.me/akash_tom" },
	{ title: "Email", icon: Email, href: "mailto:me@akashtom.com" },
];
</script>

<template>
	<a
		v-for="link in socialLinks"
		:href="link.href"
		:title="link.title"
		target="_blank"
		rel="noopener"
		class="flex items-center space-x-3 !no-underline group"
	>
		<component
			:is="link.icon"
			class="h-5 w-5 fill-gray-200 group-hover:fill-amber-300 group-active:fill-amber-300"
		/>
		<span class="sm:hidden">{{ link.title }}</span>
	</a>
</template>
