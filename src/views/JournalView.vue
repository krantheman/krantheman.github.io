<script setup>
import { posts } from "@/data.js";
</script>

<template>
	<router-link
		v-for="post in posts"
		:key="post.id"
		class="space-y-1 no-underline!"
		:to="`/journal/${post.link}`"
	>
		<h2 class="mt-8">{{ post.title }}</h2>
		<h6>{{ post.date }}</h6>
		<p class="text-gray-100">{{ post.description }}</p>
	</router-link>
</template>
