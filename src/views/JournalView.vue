<script setup>
import { posts } from "@/data.js";
</script>

<template>
	<div class="space-y-8">
		<div v-for="post in posts">
			<router-link class="space-y-1 no-underline!" :to="`/journal/${post.link}`">
				<h4>{{ post.title }}</h4>
				<h6>{{ post.date }}</h6>
				<p class="text-gray-100">{{ post.description }}</p>
			</router-link>
		</div>
	</div>
</template>
