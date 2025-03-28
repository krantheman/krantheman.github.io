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
			path: "/blogs",
			name: "Blogs",
			component: () => import("./views/BlogsView.vue"),
		},
		{
			path: "/blogs/:name",
			name: "Blog",
			component: () => import("./views/BlogView.vue"),
			props: true,
		},
		{
			path: "/gallery",
			name: "Gallery",
			component: () => import("./views/GalleryView.vue"),
		},
		{
			path: "/about",
			name: "About",
			component: () => import("./views/AboutView.vue"),
		},
	],
});

export default router;
