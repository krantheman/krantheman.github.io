<script setup>
import { ref, watch } from "vue";
import lqipData from "@/lqip-data.json";

const { src, originalPath, alt, loading } = defineProps({
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
	loading: {
		type: String,
		default: "lazy",
	},
});

const currentSrc = ref(null);
const placeholderSrc = ref(null);
const actualSrc = ref(null);
const isLoading = ref(true);

const findLQIPData = (imgSrc, imgPath) => {
	if (!imgSrc || typeof imgSrc !== "string") return null;

	if (imgPath && typeof imgPath === "string") {
		const normalizedPath = imgPath.replace("/src", "src");

		if (lqipData[normalizedPath]) {
			return lqipData[normalizedPath];
		}
	}

	// Fallback: Try to match by path segments
	const srcSegments = imgSrc.split("/").filter(Boolean);
	const srcFilename =
		srcSegments[srcSegments.length - 1]?.split("-")[0] + ".avif";

	// Try to match by filename and path context
	for (const [path, data] of Object.entries(lqipData)) {
		const pathParts = path.split("/");
		const lqipFilename = pathParts[pathParts.length - 1];

		// Simple filename match
		if (lqipFilename === srcFilename) {
			return data;
		}

		// Try matching by last 2-3 segments of the path
		const lqipSegments = pathParts.slice(-3).join("/");
		if (
			imgSrc.includes(lqipSegments.replace(/\s+/g, "%20")) ||
			imgSrc.includes(lqipSegments.replace(/\s+/g, "-"))
		) {
			return data;
		}
	}

	return null;
};

const loadImage = (imgSrc, imgPath) => {
	if (!imgSrc || typeof imgSrc !== "string") {
		currentSrc.value = null;
		actualSrc.value = null;
		placeholderSrc.value = null;
		isLoading.value = false;
		return;
	}

	// Try to find LQIP data for this image
	const lqip = findLQIPData(imgSrc, imgPath);

	if (lqip) {
		// Set placeholder first, then swap to actual image
		placeholderSrc.value = lqip.placeholder;
		actualSrc.value = imgSrc;
		currentSrc.value = lqip.placeholder;
		isLoading.value = true;
		// Swap to actual image after a brief delay to ensure placeholder shows
		setTimeout(() => {
			currentSrc.value = imgSrc;
		}, 0);
	} else {
		// No LQIP data, load image directly
		placeholderSrc.value = null;
		actualSrc.value = imgSrc;
		currentSrc.value = imgSrc;
		isLoading.value = false;
	}
};

const handleImageLoad = () => {
	isLoading.value = false;
};

const handleImageError = () => {
	isLoading.value = false;
};

// Watch for changes in image source and path
watch(
	[() => src, () => originalPath],
	([newSrc, newPath]) => {
		loadImage(newSrc, newPath);
	},
	{ immediate: true },
);
</script>

<template>
	<img
		:src="currentSrc"
		:alt
		:loading
		@load="handleImageLoad"
		@error="handleImageError"
	/>
</template>
