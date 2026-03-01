<script setup>
import { ref, onMounted } from "vue";
import { placeSubtitles } from "@/data.js";
import { getDate } from "@/utils.js";

const places = ref([]);

onMounted(() => {
	const placeThumbnails = import.meta.glob("@/assets/images/*/00.avif", {
		eager: true,
	});

	const placeMap = new Map();

	for (const path in placeThumbnails) {
		const pathParts = path.split("/");
		const placeName = pathParts[pathParts.length - 2];

		placeMap.set(placeName, {
			id: placeName,
			title: placeName.split(" ")[1],
			date: getDate(placeName.split(" ")[0]),
			subtitle: placeSubtitles[placeName] || "",
			thumbnail: {
				id: path,
				src: placeThumbnails[path].default,
				alt: placeName,
			},
		});
	}

	places.value = Array.from(placeMap.values()).reverse();
});
</script>

<template>
	<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
		<router-link
			v-for="place in places"
			:key="place.id"
			class="no-underline! group"
			:to="`/places/${place.id}`"
		>
			<div class="flex items-baseline">
				<h3 class="mb-0!">{{ place.title }}</h3>
				<h6 class="ml-2 mb-0!">{{ place.date }}</h6>
			</div>
			<p v-if="place.subtitle" class="mt-0! mb-3 text-gray-100">
				{{ place.subtitle }}
			</p>
			<div class="overflow-hidden rounded-md aspect-3/2 relative">
				<img
					v-if="place.thumbnail"
					:src="place.thumbnail.src"
					:alt="place.title"
					loading="lazy"
					class="w-full h-full object-cover group-hover:opacity-80"
				/>
				/>
			</div>
		</router-link>
	</div>
</template>
