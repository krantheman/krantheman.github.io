import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: "/",
			name: "Home",
			component: () => import("@/views/HomeView.vue"),
		},
		{
			path: "/places",
			name: "Places",
			component: () => import("@/views/PlacesView.vue"),
		},
		{
			path: "/places/:name",
			name: "Place",
			component: () => import("@/views/PlaceView.vue"),
			props: true,
		},
		{
			path: "/journal",
			name: "Journal",
			component: () => import("@/views/JournalView.vue"),
		},
		{
			path: "/journal/:name",
			name: "Post",
			component: () => import("@/views/PostView.vue"),
			props: true,
		},
		{
			path: "/work",
			name: "Work",
			component: () => import("@/views/WorkView.vue"),
		},
	],
});

router.afterEach((to) => {
	const titleParts = [];

	// Place page: "Ladakh '24"
	if (to.name === "Place" && to.params.name) {
		const [yearMonth, ...titleWords] = to.params.name.split(" ");
		const year = yearMonth.split("-")[0];
		const placeTitle = titleWords.join(" ");
		titleParts.push(`${placeTitle} '${year}`);
	}
	// Album within place: "Lizard and man"
	else if (to.query?.album) {
		titleParts.push(to.query.album.slice(3));
	}
	// Post page: capitalize title from slug
	else if (to.params.name) {
		const postTitle = to.params.name
			.split("-")
			.join(" ")
			.replace(/^\w/, (c) => c.toUpperCase());
		titleParts.push(postTitle);
	}
	// Other named routes: "Akash's Places"
	else if (to.name && to.name !== "Home") {
		titleParts.push(`Akash's ${to.name}`);
	}
	// Home page
	else {
		titleParts.push("Akash's Home");
	}

	document.title = titleParts.join(" - ");
});

export default router;
