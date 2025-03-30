import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: "/",
			name: "Home",
			component: () => import("./views/HomeView.vue"),
		},
		{
			path: "/gallery",
			name: "Gallery",
			component: () => import("./views/GalleryView.vue"),
		},
		{
			path: "/blog",
			name: "Blogs",
			component: () => import("./views/BlogsView.vue"),
		},
		{
			path: "/blog/:name",
			name: "Blog",
			component: () => import("./views/BlogView.vue"),
			props: true,
		},
		{
			path: "/projects",
			name: "Projects",
			component: () => import("./views/ProjectsView.vue"),
		},
	],
});

export default router;
