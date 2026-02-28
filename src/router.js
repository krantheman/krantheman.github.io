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
	document.title =
		to.query?.group?.slice(3) ||
		to.params.name
			?.split("-")
			.join(" ")
			.replace(/^\w/, (c) => c.toUpperCase()) ||
		`Akash's ${to.name || "Home"}`;
});

export default router;
