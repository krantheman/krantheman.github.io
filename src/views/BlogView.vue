<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import markdownIt from "markdown-it";

const route = useRoute();
const router = useRouter();
const md = markdownIt();

const htmlContent = ref("");

onMounted(async () => {
	const filePath = `/blogs/${route.path.split("/").at(-1)}.md`;
	const fileContent = await fetch(filePath).then((res) => res.text());
	if (fileContent.includes("<!doctype html>")) router.replace("/blogs");
	htmlContent.value = md.render(fileContent);
});
</script>

<template>
	<div v-html="htmlContent" />
</template>
