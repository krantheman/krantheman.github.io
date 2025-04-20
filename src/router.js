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
			path: "/gallery",
			name: "Gallery",
			component: () => import("@/views/GalleryView.vue"),
		},
		{
			path: "/blog",
			name: "Blog",
			component: () => import("@/views/BlogView.vue"),
		},
		{
			path: "/blog/:name",
			name: "Post",
			component: () => import("@/views/PostView.vue"),
			props: true,
		},
		{
			path: "/projects",
			name: "Projects",
			component: () => import("@/views/ProjectsView.vue"),
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
