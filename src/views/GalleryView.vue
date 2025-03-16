<script setup>
import ChevronLeft from "@/components/icons/ChevronLeft.vue";
import ChevronRight from "@/components/icons/ChevronRight.vue";
import {
	computed,
	ref,
	reactive,
	onMounted,
	onBeforeUnmount,
	watch,
} from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const albums = ref([]);
const selectedGroup = ref(null);
const selectedImage = ref(null);
const currentIdx = reactive({ album: 0, group: 0, image: 0 });

const findImageIndices = (image) => {
	for (let albumIdx = 0; albumIdx < albums.value.length; albumIdx++) {
		const album = albums.value[albumIdx];

		for (let groupIdx = 0; groupIdx < album.groups.length; groupIdx++) {
			const group = album.groups[groupIdx];
			const imageIdx = group.images.findIndex((img) => img.id === image.id);

			if (imageIdx !== -1) return { albumIdx, groupIdx, imageIdx };
		}
	}
	return { albumIdx: 0, groupIdx: 0, imageIdx: 0 };
};

const openPreview = (group, image) => {
	selectedGroup.value = group;
	selectedImage.value = image || group.images[0];

	const { albumIdx, groupIdx, imageIdx } = findImageIndices(
		selectedImage.value,
	);

	currentIdx.album = albumIdx;
	currentIdx.group = groupIdx;
	currentIdx.image = imageIdx || 0;

	updateUrl(currentIdx.album, currentIdx.group, currentIdx.image);

	document.addEventListener("keydown", handleKeydown);
};

const closePreview = () => {
	selectedGroup.value = null;
	selectedImage.value = null;
	document.removeEventListener("keydown", handleKeydown);
	updateUrl(null, null, null);
};

const updateUrl = (albumIdx, groupIdx, imageIdx) => {
	const query = {};

	if (albumIdx !== null && groupIdx !== null) {
		const album = albums.value[albumIdx];
		const group = album.groups[groupIdx];

		query.album = album.id;
		query.group = group.id;

		if (imageIdx !== null) query.image = imageIdx;
	}

	router.replace({ query });
};

const nextImage = () => {
	const album = albums.value[currentIdx.album];
	const group = album.groups[currentIdx.group];

	if (currentIdx.image < group.images.length - 1) currentIdx.image++;
	else if (currentIdx.group < album.groups.length - 1) {
		currentIdx.group++;
		currentIdx.image = 0;
	} else if (currentIdx.album < albums.value.length - 1) {
		currentIdx.album++;
		currentIdx.group = 0;
		currentIdx.image = 0;
	} else return;

	const newAlbum = albums.value[currentIdx.album];
	selectedGroup.value = newAlbum.groups[currentIdx.group];
	selectedImage.value = selectedGroup.value.images[currentIdx.image];
	updateUrl(currentIdx.album, currentIdx.group, currentIdx.image);
};

const prevImage = () => {
	if (currentIdx.image > 0) currentIdx.image--;
	else if (currentIdx.group > 0) {
		currentIdx.group--;
		selectedGroup.value =
			albums.value[currentIdx.album].groups[currentIdx.group];
		currentIdx.image = selectedGroup.value.images.length - 1;
	} else if (currentIdx.album > 0) {
		currentIdx.album--;
		const prevAlbum = albums.value[currentIdx.album];
		currentIdx.group = prevAlbum.groups.length - 1;
		selectedGroup.value = prevAlbum.groups[currentIdx.group];
		currentIdx.image = selectedGroup.value.images.length - 1;
	} else return;

	selectedImage.value = selectedGroup.value.images[currentIdx.image];
	updateUrl(currentIdx.album, currentIdx.group, currentIdx.image);
};

const isFirstImage = computed(
	() =>
		currentIdx.album === 0 && currentIdx.group === 0 && currentIdx.image === 0,
);

const isLastImage = computed(() => {
	const lastAlbumIdx = albums.value.length - 1;
	const lastGroupIdx = albums.value[lastAlbumIdx].groups.length - 1;
	const lastImageIdx =
		albums.value[lastAlbumIdx].groups[lastGroupIdx].images.length - 1;

	return (
		currentIdx.album === lastAlbumIdx &&
		currentIdx.group === lastGroupIdx &&
		currentIdx.image === lastImageIdx
	);
});

const handleKeydown = (event) => {
	if (event.key === "Escape") closePreview();
	else if (event.key === "ArrowRight") nextImage();
	else if (event.key === "ArrowLeft") prevImage();
};

onBeforeUnmount(() => document.removeEventListener("keydown", handleKeydown));

const checkQueryParams = () => {
	const { album, group, image } = route.query;
	if (!(album && group)) return;

	const albumIdx = albums.value.findIndex((a) => a.id === album);
	if (albumIdx === -1) return;

	const albumObj = albums.value[albumIdx];
	const groupIdx = albumObj.groups.findIndex((a) => a.id === group);
	if (groupIdx === -1) return;

	const groupObj = albumObj.groups[groupIdx];
	const imageIdx = image ? parseInt(image) : 0;
	if (!(albumObj && groupObj)) return;

	selectedGroup.value = groupObj;
	selectedImage.value = groupObj.images[imageIdx] || groupObj.images[0];

	currentIdx.album = albumIdx;
	currentIdx.group = groupIdx;
	currentIdx.image = imageIdx;

	document.addEventListener("keydown", handleKeydown);
};

watch(() => route.query, checkQueryParams, { immediate: true });

onMounted(async () => {
	const imageModules = import.meta.glob("../assets/images/**/*.avif");

	const albumMap = new Map();

	for (const path in imageModules) {
		const pathParts = path.split("/");
		const albumName = pathParts[pathParts.length - 3];
		const groupName = pathParts[pathParts.length - 2];
		const fileName = pathParts[pathParts.length - 1];

		const imageModule = await imageModules[path]();

		const image = {
			id: fileName,
			src: imageModule.default,
			alt: fileName.split(".")[0],
		};

		if (!albumMap.has(albumName))
			albumMap.set(albumName, {
				id: albumName,
				title: albumName.split(" ")[1],
				date: getDate(albumName.split(" ")[0]),
				groups: [],
			});

		const album = albumMap.get(albumName);

		let group = album.groups.find((a) => a.id === groupName);
		if (!group) {
			group = { id: groupName, images: [] };
			album.groups.push(group);
		}

		group.images.push(image);
	}

	albums.value = Array.from(albumMap.values());
	checkQueryParams();
});

const getDate = (date) => {
	const [year, month] = date.split("-");
	const monthNames = [
		"Jan",
		"Feb",
		"Mar",
		"Apr",
		"May",
		"Jun",
		"Jul",
		"Aug",
		"Sep",
		"Oct",
		"Nov",
		"Dec",
	];

	const monthIndex = parseInt(month, 10) - 1;
	return `${monthNames[monthIndex]} 20${year}`;
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
	<div v-for="album in albums" :key="album.id">
		<div class="flex items-baseline">
			<h3 class="!mt-0">{{ album.title }}</h3>
			<h6 class="ml-2.5">{{ album.date }}</h6>
		</div>

		<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
			<div
				v-for="group in album.groups"
				:key="group.id"
				class="cursor-pointer overflow-hidden rounded-md aspect-3/2 relative group"
				@click="openPreview(group)"
			>
				<img
					:src="group.images[0].src"
					:alt="group.id"
					class="w-full h-full object-cover"
					loading="lazy"
				/>

				<div class="absolute bottom-0 left-0 p-4">
					<h4 class="!my-0">{{ group.id }}</h4>
					<span class="text-sm">{{ group.images.length }} items</span>
				</div>
			</div>
		</div>
	</div>

	<div
		v-if="selectedGroup && selectedImage"
		class="fixed inset-0 flex items-center justify-center z-50 bg-black"
		@click="closePreview"
		@touchstart="handleTouchStart"
		@touchend="handleTouchEnd"
	>
		<button
			class="fixed left-4 top-1/2 transform -translate-y-1/2 p-3 cursor-pointer hidden sm:block"
			@click.stop="prevImage"
			aria-label="Previous image"
			:disabled="isFirstImage"
			:class="{ 'opacity-50 !cursor-default': isFirstImage }"
		>
			<ChevronLeft class="h-6 w-6" />
		</button>

		<button
			class="fixed right-4 top-1/2 transform -translate-y-1/2 p-3 cursor-pointer hidden sm:block"
			@click.stop="nextImage"
			aria-label="Next image"
			:disabled="isLastImage"
			:class="{ 'opacity-50 !cursor-default': isLastImage }"
		>
			<ChevronRight class="h-6 w-6" />
		</button>

		<p class="fixed top-4 flex justify-center !my-0">
			{{ selectedGroup.id }}
		</p>

		<div class="fixed bottom-4 left-1/2 text-sm">
			{{ currentIdx.image + 1 }} / {{ selectedGroup.images.length }}
		</div>

		<img
			v-if="selectedImage"
			:src="selectedImage.src"
			:alt="selectedImage.alt"
			class="sm:max-w-[88%] max-h-[88vh] block"
			@click.stop
		/>
	</div>
</template>
