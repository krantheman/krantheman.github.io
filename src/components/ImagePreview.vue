<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from "vue";
import ChevronLeft from "@/components/icons/ChevronLeft.vue";
import ChevronRight from "@/components/icons/ChevronRight.vue";
import LQIPImage from "@/components/LQIPImage.vue";

const { place, previewIdx } = defineProps({
	place: {
		type: Object,
		required: true,
	},
	previewIdx: {
		type: Object,
		required: true,
	},
});

const emit = defineEmits(["updateUrl", "close"]);

const selectedAlbum = ref(null);
const selectedImage = ref(null);

onMounted(() => {
	document.addEventListener("keydown", handleKeydown);
	document.body.classList.add("overflow-hidden");
	window.addEventListener("popstate", closePreview);
});

onBeforeUnmount(() => {
	document.removeEventListener("keydown", handleKeydown);
	document.body.classList.remove("overflow-hidden");
	window.removeEventListener("popstate", closePreview);
});

watch(
	[
		() => previewIdx.album,
		() => previewIdx.image,
		() => place?.albums[previewIdx.album]?.images,
	],
	() => {
		if (place && place.albums.length > previewIdx.album) {
			selectedAlbum.value = place.albums[previewIdx.album];
			if (selectedAlbum.value.images?.length > previewIdx.image) {
				selectedImage.value = selectedAlbum.value.images[previewIdx.image];
			}
		}
	},
	{ immediate: true, deep: true },
);

const nextImage = () => {
	const album = place.albums[previewIdx.album];

	if (previewIdx.image < album.images.length - 1) previewIdx.image++;
	else if (previewIdx.album < place.albums.length - 1) {
		previewIdx.album++;
		previewIdx.image = 0;
	} else return;

	emit("updateUrl", previewIdx.album, previewIdx.image);
};

const prevImage = () => {
	if (previewIdx.image > 0) previewIdx.image--;
	else if (previewIdx.album > 0) {
		previewIdx.album--;
		const prevAlbum = place.albums[previewIdx.album];
		const imageCount =
			prevAlbum.images.length || prevAlbum.imagePaths?.length || 0;
		previewIdx.image = Math.max(0, imageCount - 1);
	} else return;

	emit("updateUrl", previewIdx.album, previewIdx.image);
};

const closePreview = () => {
	emit("updateUrl", null, null);
	emit("close");
};

const isFirstImage = computed(
	() => previewIdx.album === 0 && previewIdx.image === 0,
);

const isLastImage = computed(() => {
	const lastAlbumIdx = place.albums.length - 1;
	const lastImageIdx = place.albums[lastAlbumIdx].images.length - 1;

	return previewIdx.album === lastAlbumIdx && previewIdx.image === lastImageIdx;
});

const handleKeydown = (event) => {
	if (event.key === "Escape") closePreview();
	else if (event.key === "ArrowRight") nextImage();
	else if (event.key === "ArrowLeft") prevImage();
};

const touchStartX = ref(0);
const isZooming = ref(false);

const handleTouchStart = (event) => {
	if (event.touches.length >= 2) return (isZooming.value = true);

	isZooming.value = false;
	touchStartX.value = event.touches[0].clientX;
};

const handleTouchEnd = (event) => {
	if (isZooming.value) return setTimeout(() => (isZooming.value = false), 500);

	const swipeDistance = event.changedTouches[0].clientX - touchStartX.value;
	if (Math.abs(swipeDistance) < 50) return;

	if (swipeDistance > 0) prevImage();
	else nextImage();
};
</script>

<template>
	<div
		class="fixed inset-0 flex flex-col z-50 bg-black"
		@click="closePreview"
		@touchstart="handleTouchStart"
		@touchend="handleTouchEnd"
	>
		<div class="flex-1 flex items-center justify-center p:0 sm:p-4 min-h-0">
			<LQIPImage
				v-if="selectedImage"
				:src="selectedImage.src"
				:original-path="selectedImage.id"
				:alt="selectedImage.alt"
				class="w-full h-full object-contain"
				loading="eager"
			/>
		</div>

		<div
			v-if="selectedAlbum"
			class="flex items-center justify-between p-4 sm:px-6 sm:py-4"
		>
			<p class="m-0">{{ selectedAlbum.id.split(" ").slice(1).join(" ") }}</p>

			<div class="flex items-center gap-4">
				<button
					class="cursor-pointer"
					@click.stop="prevImage"
					aria-label="Previous image"
					:disabled="isFirstImage"
					:class="{ 'opacity-30 cursor-default!': isFirstImage }"
				>
					<ChevronLeft />
				</button>

				<span class="text-sm tabular-nums w-12 text-center">
					{{ previewIdx.image + 1 }} /
					{{ selectedAlbum?.images?.length ?? "—" }}
				</span>

				<button
					class="cursor-pointer"
					@click.stop="nextImage"
					aria-label="Next image"
					:disabled="isLastImage"
					:class="{ 'opacity-30 cursor-default!': isLastImage }"
				>
					<ChevronRight />
				</button>
			</div>
		</div>
	</div>
</template>
