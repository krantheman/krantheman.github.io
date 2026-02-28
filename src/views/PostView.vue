<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import markdownIt from "markdown-it";

const { name } = defineProps(["name"]);

const router = useRouter();

const md = markdownIt();

md.renderer.rules.link_open = (tokens, idx, options, _, self) => {
	tokens[idx].attrSet("target", "_blank");
	return self.renderToken(tokens, idx, options);
};

const htmlContent = ref("");

onMounted(async () => {
	const blogFiles = import.meta.glob("@/content/posts/*.md", {
		query: "?raw",
		import: "default",
	});

	const importPath = `/src/content/posts/${name}.md`;

	if (importPath in blogFiles) {
		const fileContent = await blogFiles[importPath]();
		htmlContent.value = md.render(fileContent);
	} else router.replace("/journal");
});
</script>

<template>
	<div v-html="htmlContent" />
</template>
