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
const showPreview = ref(false);

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
	showPreview.value = true;

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
	showPreview.value = false;
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
	showPreview.value = true;

	currentIdx.album = albumIdx;
	currentIdx.group = groupIdx;
	currentIdx.image = imageIdx;

	document.addEventListener("keydown", handleKeydown);
};

watch(() => route.query, checkQueryParams, { immediate: true });

onMounted(async () => {
	const imageModules = import.meta.glob("../assets/images/**/*.avif");

	const galleryMap = new Map();

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

		if (!galleryMap.has(albumName))
			galleryMap.set(albumName, {
				id: albumName,
				date: "Aug 2024",
				groups: [],
			});

		const album = galleryMap.get(albumName);

		let group = album.groups.find((a) => a.id === groupName);
		if (!group) {
			group = {
				id: groupName,
				caption: generateCaption(groupName),
				images: [],
			};
			album.groups.push(group);
		}

		group.images.push(image);
	}

	albums.value = Array.from(galleryMap.values());
	checkQueryParams();
});

// You can replace this with actual captions from a data file or other source
function generateCaption(albumName) {
	// This is a placeholder - in a real app, you might fetch this from a JSON file or CMS
	const captions = {
		album1: "Beautiful landscapes from our trip to the mountains",
		"summer-2023": "Summer vacation photos from 2023",
		family: "Family gathering during the holidays",
	};

	// Return caption if it exists, otherwise create a generic one
	return captions[albumName] || `${albumName.replace(/-/g, " ")}`;
}
</script>

<template>
	<div class="py-8">
		<h1 class="text-center">Gallery</h1>
		<div v-for="album in albums" :key="album.id">
			<div class="flex flex-row items-baseline">
				<h2>{{ album.id }}</h2>
				<span class="text-gray-400 ml-3 text-sm">
					{{ album.date }}
				</span>
			</div>

			<div class="grid grid-cols-2 md:grid-cols-3 gap-4">
				<div
					v-for="group in album.groups"
					:key="group.id"
					class="cursor-pointer overflow-hidden rounded-md aspect-square relative group"
					@click="openPreview(group)"
				>
					<img
						v-if="group.images && group.images.length > 0"
						:src="group.images[0].src"
						:alt="group.id"
						class="w-full h-full object-cover"
						loading="lazy"
					/>

					<div
						class="absolute inset-0 bg-opacity-0 group-hover:bg-opacity-60 transition-all duration-300 flex items-end"
					>
						<div
							class="p-3 w-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"
						>
							<h3 class="font-medium">{{ group.id }}</h3>
							<p class="text-sm">{{ group.images.length }} photos</p>
						</div>
					</div>
				</div>
			</div>
		</div>

		<div
			v-if="showPreview && selectedGroup"
			class="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50"
			@click="closePreview"
		>
			<button
				class="fixed left-4 top-1/2 transform -translate-y-1/2 bg-black bg-opacity-50 rounded-full p-3 hover:bg-opacity-70 focus:outline-none cursor-pointer"
				@click.stop="prevImage"
				aria-label="Previous image"
				:disabled="currentIdx.image === 0"
				:class="{ 'opacity-50 cursor-not-allowed': currentIdx.image === 0 }"
			>
				<ChevronLeft class="h-6 w-6" />
			</button>

			<button
				class="fixed right-4 top-1/2 transform -translate-y-1/2 bg-black bg-opacity-50 rounded-full p-3 hover:bg-opacity-70 focus:outline-none cursor-pointer"
				@click.stop="nextImage"
				aria-label="Next image"
				:disabled="currentIdx.image === selectedGroup.images.length - 1"
				:class="{
					'opacity-50 cursor-not-allowed':
						currentIdx.image === selectedGroup.images.length - 1,
				}"
			>
				<ChevronRight class="h-6 w-6" />
			</button>

			<div class="fixed top-4 left-0 right-0 flex justify-between px-4">
				<div class="bg-black bg-opacity-50 px-4 py-2 rounded-md text-lg">
					{{ selectedGroup.id }}
				</div>
			</div>

			<div
				class="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-black bg-opacity-50 px-3 py-1 rounded-full text-sm"
			>
				{{ currentIdx.image + 1 }} /
				{{ selectedGroup.images.length }}
			</div>

			<div
				class="fixed bottom-16 left-1/2 transform -translate-x-1/2 max-w-lg bg-black bg-opacity-50 px-4 py-2 rounded-md text-center"
			>
				{{ selectedGroup.caption }}
			</div>

			<div class="relative max-w-[90%] max-h-[90%]" @click.stop>
				<img
					v-if="selectedImage"
					:src="selectedImage.src"
					:alt="selectedImage.alt"
					class="max-w-full max-h-[90vh] block"
				/>
			</div>
		</div>
	</div>
</template>
