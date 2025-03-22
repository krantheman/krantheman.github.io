<script setup>
import ChevronLeft from "@/components/icons/ChevronLeft.vue";
import ChevronRight from "@/components/icons/ChevronRight.vue";
import { ref, computed, onMounted, onBeforeUnmount } from "vue";

const { albums, previewIdx } = defineProps({
	albums: {
		type: Array,
		required: true,
	},
	previewIdx: {
		type: Object,
		required: true,
	},
});

const emit = defineEmits(["updateUrl", "close"]);

const selectedGroup = ref(null);
const selectedImage = ref(null);

onMounted(() => {
	const album = albums[previewIdx.album];
	if (album && album.groups.length > previewIdx.group) {
		selectedGroup.value = album.groups[previewIdx.group];
		if (selectedGroup.value.images.length > previewIdx.image)
			selectedImage.value = selectedGroup.value.images[previewIdx.image];
	}

	document.addEventListener("keydown", handleKeydown);
});

onBeforeUnmount(() => document.removeEventListener("keydown", handleKeydown));

const nextImage = () => {
	const album = albums[previewIdx.album];
	const group = album.groups[previewIdx.group];

	if (previewIdx.image < group.images.length - 1) previewIdx.image++;
	else if (previewIdx.group < album.groups.length - 1) {
		previewIdx.group++;
		previewIdx.image = 0;
	} else if (previewIdx.album < albums.length - 1) {
		previewIdx.album++;
		previewIdx.group = 0;
		previewIdx.image = 0;
	} else return;

	const newAlbum = albums[previewIdx.album];
	selectedGroup.value = newAlbum.groups[previewIdx.group];
	selectedImage.value = selectedGroup.value.images[previewIdx.image];
	emit("updateUrl", previewIdx.album, previewIdx.group, previewIdx.image);
};

const prevImage = () => {
	if (previewIdx.image > 0) previewIdx.image--;
	else if (previewIdx.group > 0) {
		previewIdx.group--;
		selectedGroup.value = albums[previewIdx.album].groups[previewIdx.group];
		previewIdx.image = selectedGroup.value.images.length - 1;
	} else if (previewIdx.album > 0) {
		previewIdx.album--;
		const prevAlbum = albums[previewIdx.album];
		previewIdx.group = prevAlbum.groups.length - 1;
		selectedGroup.value = prevAlbum.groups[previewIdx.group];
		previewIdx.image = selectedGroup.value.images.length - 1;
	} else return;

	selectedImage.value = selectedGroup.value.images[previewIdx.image];
	emit("updateUrl", previewIdx.album, previewIdx.group, previewIdx.image);
};

const closePreview = () => {
	emit("updateUrl", null, null, null);
	emit("close");
};

const isFirstImage = computed(
	() =>
		previewIdx.album === 0 && previewIdx.group === 0 && previewIdx.image === 0,
);

const isLastImage = computed(() => {
	const lastAlbumIdx = albums.length - 1;
	const lastGroupIdx = albums[lastAlbumIdx].groups.length - 1;
	const lastImageIdx =
		albums[lastAlbumIdx].groups[lastGroupIdx].images.length - 1;

	return (
		previewIdx.album === lastAlbumIdx &&
		previewIdx.group === lastGroupIdx &&
		previewIdx.image === lastImageIdx
	);
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
		class="fixed inset-0 flex z-50 bg-black"
		@click="closePreview"
		@touchstart="handleTouchStart"
		@touchend="handleTouchEnd"
	>
		<button
			class="cursor-pointer hidden sm:block ml-4 self-center"
			@click.stop="prevImage"
			aria-label="Previous image"
			:disabled="isFirstImage"
			:class="{ 'opacity-50 !cursor-default': isFirstImage }"
		>
			<ChevronLeft class="h-8 w-8" />
		</button>

		<div class="flex flex-col h-full w-full">
			<div class="flex-1 flex items-center justify-center h-0 flex-grow sm:m-4">
				<img
					v-if="selectedImage"
					:src="selectedImage.src"
					:alt="selectedImage.alt"
					loading="lazy"
					class="max-h-full max-w-full"
					@click.stop
				/>
			</div>
			<p v-if="selectedGroup" class="flex justify-center items-center">
				{{ selectedGroup.id }}
				<span class="text-gray-400 font-extralight ml-1 text-sm">
					({{ previewIdx.image + 1 }}/{{ selectedGroup.images.length }})
				</span>
			</p>
		</div>

		<button
			class="cursor-pointer hidden sm:block mr-4 self-center"
			@click.stop="nextImage"
			aria-label="Next image"
			:disabled="isLastImage"
			:class="{ 'opacity-50 !cursor-default': isLastImage }"
		>
			<ChevronRight class="h-8 w-8" />
		</button>
	</div>
</template>
