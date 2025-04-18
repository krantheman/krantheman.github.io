<script setup>
import { ref, reactive, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import ImagePreview from "@/components/ImagePreview.vue";

const route = useRoute();
const router = useRouter();

const albums = ref([]);
const showPreview = ref(false);
const previewIdx = reactive({ album: 0, group: 0, image: 0 });

onMounted(() => {
	const imageModules = import.meta.glob("@/assets/images/*/**/*.avif", {
		eager: true,
	});

	const albumMap = new Map();

	for (const path in imageModules) {
		const pathParts = path.split("/");
		const albumName = pathParts[pathParts.length - 3];
		const groupName = pathParts[pathParts.length - 2];
		const fileName = pathParts[pathParts.length - 1];

		const image = {
			id: path,
			src: imageModules[path].default,
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
			group = { id: groupName, images: [], thumbnail: null };
			album.groups.push(group);
		}

		if (fileName === "00.avif") group.thumbnail = image;
		else group.images.push(image);
	}

	albums.value = Array.from(albumMap.values()).reverse();
	checkQueryParams();
});

const checkQueryParams = () => {
	const { album, group, image } = route.query;
	if (!(album && group && image !== undefined)) return;

	const albumIdx = albums.value.findIndex((a) => a.id === album);
	if (albumIdx === -1) return;

	const albumObj = albums.value[albumIdx];
	const groupIdx = albumObj.groups.findIndex((a) => a.id === group);
	if (groupIdx === -1) return;

	const imageIdx = parseInt(image);
	if (
		isNaN(imageIdx) ||
		imageIdx < 0 ||
		imageIdx >= albumObj.groups[groupIdx].images.length
	)
		return;

	openPreview(albumIdx, groupIdx, imageIdx);
};

watch(() => route.query, checkQueryParams, { immediate: true });

const openPreview = (albumIdx, groupIdx, imageIdx = 0) => {
	previewIdx.album = albumIdx;
	previewIdx.group = groupIdx;
	previewIdx.image = imageIdx;
	showPreview.value = true;
	updateUrl(albumIdx, groupIdx, imageIdx);
	history.pushState({ preview: true }, "", window.location.href);
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
	<div v-for="(album, albumIdx) in albums" :key="album.id" class="mb-8">
		<div class="flex items-baseline">
			<h3 class="!mt-0">{{ album.title }}</h3>
			<h6 class="ml-2.5">{{ album.date }}</h6>
		</div>

		<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
			<div
				v-for="(group, groupIdx) in album.groups"
				:key="group.id"
				class="cursor-pointer overflow-hidden rounded-md aspect-3/2 relative group"
				@click="openPreview(albumIdx, groupIdx)"
			>
				<img
					:src="group.thumbnail.src"
					:alt="group.id"
					loading="lazy"
					class="w-full h-full object-cover"
				/>
				<div
					class="absolute inset-0 flex flex-col justify-end p-4 bg-gradient-to-t from-black/20 hover:from-black/50 active:from-black/50 to-transparent"
				>
					<h5 class="!my-0 sm:text-base">
						{{ group.id.split(" ").slice(1).join(" ") }}
					</h5>
					<span class="text-sm sm:text-xs">
						{{ group.images.length }} items
					</span>
				</div>
			</div>
		</div>
	</div>

	<ImagePreview
		v-if="showPreview"
		:albums="albums"
		:preview-idx="previewIdx"
		@update-url="updateUrl"
		@close="showPreview = false"
	/>
</template>
