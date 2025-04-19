<script setup>
const POSTS = [
	{
		title: "Exploring the Depths",
		date: "19th April, 2025",
		description: "Or exploring within? Kidding; former.",
	},
];
</script>

<template>
	<div class="space-y-8">
		<div v-for="post in POSTS">
			<router-link
				class="space-y-1 !no-underline"
				:to="`/blog/${post.title.toLowerCase().replace(/ /g, '-')}`"
			>
				<h4>{{ post.title }}</h4>
				<h6>{{ post.date }}</h6>
				<p class="text-gray-200">{{ post.description }}</p>
			</router-link>
		</div>
	</div>
</template>
