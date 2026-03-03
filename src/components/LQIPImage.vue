<script setup>
import { computed } from "vue";
import { useLQIP } from "@/composables.js";

const {
	src,
	originalPath,
	alt,
	class: className,
	loading,
} = defineProps({
	src: {
		type: String,
		required: true,
	},
	originalPath: {
		type: String,
		default: null,
	},
	alt: {
		type: String,
		default: "",
	},
	class: {
		type: String,
		default: "",
	},
	loading: {
		type: String,
		default: "lazy",
	},
});

const { currentSrc, isLoading } = useLQIP(
	computed(() => src),
	computed(() => originalPath),
);
</script>

<template>
	<div :class="['overflow-hidden', className]">
		<img
			:src="currentSrc"
			:alt
			:loading
			:class="['w-full h-full', { 'blur-sm': isLoading }]"
		/>
	</div>
</template>
