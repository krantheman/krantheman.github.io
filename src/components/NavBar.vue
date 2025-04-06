<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { RouterLink } from "vue-router";
import Socials from "@/components/Socials.vue";
import ChevronDown from "@/components/icons/ChevronDown.vue";

const websiteLinks = [
	{ name: "Home", path: "/" },
	{ name: "Gallery", path: "/gallery" },
	{ name: "Blog", path: "/blog" },
	{ name: "Projects", path: "/projects" },
];

const socialsOpen = ref(false);

const toggleSocials = () => {
	socialsOpen.value = !socialsOpen.value;
};

const handleClickOutside = () => {
	if (socialsOpen.value) socialsOpen.value = false;
};

onMounted(() => document.addEventListener("click", handleClickOutside));

onBeforeUnmount(() =>
	document.removeEventListener("click", handleClickOutside),
);
</script>

<template>
	<header class="sticky top-0 bg-[rgb(20,20,20)] z-20">
		<nav class="flex items-center py-4">
			<div class="flex w-full sm:w-auto justify-between sm:space-x-8">
				<RouterLink
					v-for="link in websiteLinks"
					:to="link.path"
					class="font-medium"
					:class="{
						'!no-underline': $route.path.split('/')[1] !== link.path.slice(1),
					}"
				>
					{{ link.name }}
				</RouterLink>
				<button
					class="font-medium cursor-pointer active:text-sky-200 sm:hidden flex items-center gap-1"
					@click.stop="toggleSocials"
				>
					Socials
					<ChevronDown
						class="transition-transform duration-300"
						:class="{ 'rotate-[-180deg]': socialsOpen }"
					/>
				</button>
			</div>
			<div class="sm:flex items-center space-x-8 ml-auto hidden">
				<Socials />
			</div>
		</nav>

		<div
			class="sm:hidden fixed left-0 right-0 bg-[rgb(20,20,20)] z-20 flex flex-col space-y-4 px-4 shadow-lg overflow-hidden transition-all duration-300 ease-linear"
			:class="socialsOpen ? 'max-h-80 py-4' : 'max-h-0 py-0'"
			@click.stop
		>
			<Socials />
		</div>
	</header>
</template>
