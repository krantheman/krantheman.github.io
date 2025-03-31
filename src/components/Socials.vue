<script setup>
import Github from "@/components/icons/Github.vue";
import Instagram from "@/components/icons/Instagram.vue";
import Linkedin from "@/components/icons/Linkedin.vue";
import Telegram from "@/components/icons/Telegram.vue";
import Email from "@/components/icons/Email.vue";

const socialLinks = [
	{ icon: Github, href: "https://github.com/krantheman" },
	{ icon: Instagram, href: "https://www.instagram.com/monsieur_le_tom/" },
	{ icon: Linkedin, href: "https://www.linkedin.com/in/akash-tom/" },
	{ icon: Telegram, href: "https://t.me/akash_tom" },
	{ icon: Email, href: "mailto:me@akashtom.com" },
];
</script>

<template>
	<a
		v-for="link in socialLinks"
		:href="link.href"
		target="_blank"
		rel="noopener"
	>
		<component
			:is="link.icon"
			class="h-4.5 w-4.5 fill-gray-200 hover:fill-sky-200 active:fill-sky-200"
		/>
	</a>
</template>
