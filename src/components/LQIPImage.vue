<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import lqipData from "@/lqip-data.json";

const { src, originalPath, alt } = defineProps({
	src: { type: String, required: true },
	originalPath: { type: String, default: null },
	alt: { type: String, default: "" },
});

const currentSrc = ref(null);
const placeholderSrc = ref(null);
const actualSrc = ref(null);
const width = ref(null);
const height = ref(null);

const imageAspect = computed(() =>
	width.value && height.value ? (width.value / height.value).toFixed(3) : null,
);

const viewportWidth = ref(window.innerWidth);
const viewportHeight = ref(window.innerHeight);
const viewportAspect = computed(() =>
	(viewportWidth.value / (viewportHeight.value - 57)).toFixed(3),
);

const updateViewport = () => {
	viewportWidth.value = window.innerWidth;
	viewportHeight.value = window.innerHeight;
};

onMounted(() => window.addEventListener("resize", updateViewport));
onUnmounted(() => window.removeEventListener("resize", updateViewport));

const findLQIPData = (imgSrc, imgPath) => {
	if (!imgSrc || typeof imgSrc !== "string") return null;

	if (imgPath && typeof imgPath === "string") {
		const normalizedPath = imgPath.replace("/src", "src");

		if (lqipData[normalizedPath]) return lqipData[normalizedPath];
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
		if (lqipFilename === srcFilename) return data;

		// Try matching by last 2-3 segments of the path
		const lqipSegments = pathParts.slice(-3).join("/");
		if (
			imgSrc.includes(lqipSegments.replace(/\s+/g, "%20")) ||
			imgSrc.includes(lqipSegments.replace(/\s+/g, "-"))
		)
			return data;
	}

	return null;
};

const loading = ref(true);

const loadImage = (imgSrc, imgPath) => {
	loading.value = true;
	if (!imgSrc || typeof imgSrc !== "string") {
		currentSrc.value = null;
		actualSrc.value = null;
		placeholderSrc.value = null;
		return;
	}

	// Try to find LQIP data for this image
	const lqip = findLQIPData(imgSrc, imgPath);

	if (lqip) {
		// Set placeholder first, then swap to actual image
		placeholderSrc.value = lqip.placeholder;
		actualSrc.value = imgSrc;
		currentSrc.value = lqip.placeholder;
		width.value = lqip.width;
		height.value = lqip.height;
		// Swap to actual image after a brief delay to ensure placeholder shows
		setTimeout(() => (currentSrc.value = imgSrc), 0);
	} else {
		// No LQIP data, load image directly
		placeholderSrc.value = null;
		actualSrc.value = imgSrc;
		currentSrc.value = imgSrc;
	}
};

// Watch for changes in image source and path
watch(
	[() => src, () => originalPath],
	([newSrc, newPath]) => loadImage(newSrc, newPath),
	{ immediate: true },
);
</script>

<template>
	<div
		class="overflow-hidden"
		:class="imageAspect > viewportAspect ? 'w-full h-auto' : 'h-full w-auto'"
	>
		<img
			:src="currentSrc"
			:alt="alt"
			class="h-full w-full object-cover scale-102"
			:class="[loading ? 'blur-md' : 'transition-all duration-300 ease-in']"
			@load="loading = false"
		/>
	</div>
</template>
