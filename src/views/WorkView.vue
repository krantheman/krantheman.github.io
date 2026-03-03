<script setup>
import { work } from "@/data.js";
</script>

<template>
	<a
		v-for="project in work"
		:key="project.id"
		class="space-y-1 no-underline!"
		:href="project.link"
		target="_blank"
	>
		<h3 class="mt-8">{{ project.title }}</h3>
		<h6>{{ project.date }}</h6>
		<p class="text-gray-100">{{ project.description }}</p>
	</a>
</template>
