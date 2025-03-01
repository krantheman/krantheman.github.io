<script setup>
const BLOGS = [
	{
		title: "Exploring the Depths",
		date: "1st March, 2025",
		description: "Or exploring myself? Kidding. Former.",
	},
	{
		title: "The Great Outdoors",
		date: "20th February, 2025",
		description: "A tale of the wild and the free.",
	},
	{
		title: "The Great Indoors",
		date: "10th February, 2025",
		description: "A tale of the wild and the free.",
	},
];
</script>

<template>
	<div class="space-y-8">
		<div v-for="blog in BLOGS">
			<router-link
				class="hover:text-sky-300 space-y-1 !no-underline"
				:to="`/blogs/${blog.title.toLowerCase().replace(/ /g, '-')}`"
			>
				<h3>{{ blog.title }}</h3>
				<h6 class="text-gray-300">{{ blog.date }}</h6>
				<p class="text-gray-300">{{ blog.description }}</p>
			</router-link>
		</div>
	</div>
</template>
