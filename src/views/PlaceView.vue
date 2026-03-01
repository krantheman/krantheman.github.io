<script setup>
import { ref, reactive, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import ImagePreview from "@/components/ImagePreview.vue";
import { getDate } from "@/utils.js";
import { placeSubtitles } from "@/data.js";

const route = useRoute();
const router = useRouter();

const place = ref(null);
const showPreview = ref(false);
const previewIdx = reactive({ album: 0, image: 0 });

onMounted(async () => {
	const placeId = route.params.name;
	const imageModules = import.meta.glob("@/assets/images/*/**/*.avif");

	const albumMap = new Map();

	const thumbnailPromises = [];

	for (const path in imageModules) {
		const pathParts = path.split("/");
		const placeName = pathParts[pathParts.length - 3];
		if (placeName !== placeId) continue;

		const albumName = pathParts[pathParts.length - 2];
		const fileName = pathParts[pathParts.length - 1];

		if (!albumMap.has(albumName)) {
			albumMap.set(albumName, {
				id: albumName,
				images: [],
				imagePaths: [],
				thumbnail: null,
				imagesLoaded: false,
			});
		}

		const album = albumMap.get(albumName);

		if (fileName === "00.avif") {
			thumbnailPromises.push(
				imageModules[path]().then((mod) => {
					album.thumbnail = { id: path, src: mod.default, alt: "00" };
				}),
			);
		} else {
			album.imagePaths.push({ path, fileName, loader: imageModules[path] });
		}
	}

	await Promise.all(thumbnailPromises);

	if (albumMap.size > 0) {
		place.value = {
			id: placeId,
			title: placeId.split(" ")[1],
			date: getDate(placeId.split(" ")[0]),
			subtitle: placeSubtitles[placeId] || "",
			albums: Array.from(albumMap.values()),
		};
	}

	checkQueryParams();
});

const checkQueryParams = () => {
	if (!place.value) return;

	const { album, image } = route.query;
	if (!(album && image !== undefined)) return;

	const albumIdx = place.value.albums.findIndex((a) => a.id === album);
	if (albumIdx === -1) return;

	const imageIdx = parseInt(image);
	if (
		isNaN(imageIdx) ||
		imageIdx < 0 ||
		imageIdx >= place.value.albums[albumIdx].images.length
	)
		return;

	openPreview(albumIdx, imageIdx);
};

watch(() => route.query, checkQueryParams, { immediate: true });

const loadAlbumImages = async (album) => {
	if (album.imagesLoaded) return;

	const loaded = await Promise.all(
		album.imagePaths.map(({ path, fileName, loader }) =>
			loader().then((mod) => ({
				id: path,
				src: mod.default,
				alt: fileName.split(".")[0],
			})),
		),
	);
	album.images = loaded;
	album.imagesLoaded = true;
};

watch(
	() => previewIdx.album,
	(newAlbumIdx) => {
		if (!place.value || newAlbumIdx === null) return;

		const album = place.value.albums[newAlbumIdx];
		if (!album) return;

		loadAlbumImages(album);
	},
);

const openPreview = async (albumIdx, imageIdx = 0) => {
	const album = place.value.albums[albumIdx];

	await loadAlbumImages(album);

	previewIdx.album = albumIdx;
	previewIdx.image = imageIdx;
	showPreview.value = true;
	updateUrl(albumIdx, imageIdx);
	history.pushState({ preview: true }, "", window.location.href);
};

const updateUrl = (albumIdx, imageIdx) => {
	const query = {};

	if (albumIdx !== null) {
		const album = place.value.albums[albumIdx];
		query.album = album.id;

		if (imageIdx !== null) query.image = imageIdx;
	}

	router.replace({ query });
};
</script>

<template>
	<div v-if="place">
		<div class="flex items-baseline">
			<h1 class="mb-0!">{{ place.title }}</h1>
			<h6 class="ml-2.5 mb-0!">{{ place.date }}</h6>
		</div>
		<p class="mb-8 mt-1">{{ place.subtitle }}</p>

		<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
			<div
				v-for="(album, albumIdx) in place.albums"
				:key="album.id"
				class="cursor-pointer overflow-hidden rounded-md aspect-3/2 relative group"
				@click="openPreview(albumIdx)"
			>
				<img
					:src="album.thumbnail.src"
					:alt="album.id"
					loading="lazy"
					class="w-full h-full object-cover group-hover:opacity-80"
				/>
				<div class="absolute inset-0 flex flex-col justify-end p-5">
					<h5 class="my-0! text-shadow">
						{{ album.id.split(" ").slice(1).join(" ") }}
					</h5>
					<span class="text-sm text-shadow">
						{{ album.imagePaths.length }} items
					</span>
				</div>
			</div>
		</div>

		<ImagePreview
			v-if="showPreview"
			:place="place"
			:preview-idx="previewIdx"
			@update-url="updateUrl"
			@close="showPreview = false"
		/>
	</div>
</template>

<style scoped>
.text-shadow {
	text-shadow:
		0 0 8px rgba(0, 0, 0, 0.4),
		0 0 4px rgba(0, 0, 0, 0.3);
}
</style>
