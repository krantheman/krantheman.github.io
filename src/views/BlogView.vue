<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import markdownIt from "markdown-it";

const route = useRoute();
const filePath = `/blogs/${route.path.split("/").at(-1)}.md`;
const htmlContent = ref();

onMounted(async () => {
	const fileContent = await fetch(filePath).then((res) => res.text());
	htmlContent.value = markdownIt().render(fileContent);
});
</script>

<template>
	<div v-html="htmlContent" />
</template>
