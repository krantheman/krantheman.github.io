<script setup>
const BLOGS = [
	{
		title: "Exploring the Depths",
		date: "1st March, 2025",
		description: "Or exploring myself? Kidding; former.",
	},
];
</script>

<template>
	<div class="space-y-8">
		<div v-for="blog in BLOGS">
			<router-link
				class="space-y-1 !no-underline"
				:to="`/blogs/${blog.title.toLowerCase().replace(/ /g, '-')}`"
			>
				<h3>{{ blog.title }}</h3>
				<h6>{{ blog.date }}</h6>
				<p class="text-gray-200">{{ blog.description }}</p>
			</router-link>
		</div>
	</div>
</template>
