<script setup>
import ChevronLeft from "@/components/icons/ChevronLeft.vue";
import ChevronRight from "@/components/icons/ChevronRight.vue";
import { ref, reactive, onMounted, onBeforeUnmount, watch } from "vue";
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
	const currentGroup = albums.value[currentIdx.album].groups[currentIdx.group];
	if (currentIdx.image >= currentGroup.images.length - 1) return;

	currentIdx.image++;
	selectedImage.value = currentGroup.images[currentIdx.image];

	updateUrl(currentIdx.album, currentIdx.group, currentIdx.image);
};

const prevImage = () => {
	if (currentIdx.image <= 0) return;

	currentIdx.image--;
	selectedImage.value =
		albums.value[currentIdx.album].groups[currentIdx.group].images[
			currentIdx.image
		];

	updateUrl(currentIdx.album, currentIdx.group, currentIdx.image);
};

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
				class="cursor-pointer overflow-hidden rounded-md aspect-6/5 relative group"
				@click="openPreview(group)"
			>
				<img
					:src="group.images[0].src"
					:alt="group.id"
					class="w-full h-full object-cover"
					loading="lazy"
				/>

				<div
					class="absolute bottom-0 left-0 p-4 duration-300 ease-in-out group-hover:bottom-0.5"
				>
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
	>
		<button
			class="fixed left-4 top-1/2 transform -translate-y-1/2 rounded-full p-3 cursor-pointer"
			@click.stop="prevImage"
			aria-label="Previous image"
			:disabled="currentIdx.image === 0"
			:class="{ 'opacity-50 !cursor-default': currentIdx.image === 0 }"
		>
			<ChevronLeft class="h-6 w-6" />
		</button>

		<button
			class="fixed right-4 top-1/2 transform -translate-y-1/2 rounded-full p-3 cursor-pointer"
			@click.stop="nextImage"
			aria-label="Next image"
			:disabled="currentIdx.image === selectedGroup.images.length - 1"
			:class="{
				'opacity-50 !cursor-default':
					currentIdx.image === selectedGroup.images.length - 1,
			}"
		>
			<ChevronRight class="h-6 w-6" />
		</button>

		<p class="fixed top-4 left-0 right-0 flex justify-center !my-0">
			{{ selectedGroup.id }}
		</p>

		<div class="fixed bottom-4 left-1/2 text-sm">
			{{ currentIdx.image + 1 }} / {{ selectedGroup.images.length }}
		</div>

		<img
			v-if="selectedImage"
			:src="selectedImage.src"
			:alt="selectedImage.alt"
			class="max-w-[87%] max-h-[87vh] block"
			@click.stop
		/>
	</div>
</template>
