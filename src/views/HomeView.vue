<script setup>
import LQIPImage from "@/components/LQIPImage.vue";
import Socials from "@/components/Socials.vue";
import me from "@/assets/images/me.jpg";
</script>

<template>
	<div class="flex items-start flex-col sm:flex-row sm:py-20 gap-8">
		<LQIPImage
			:src="me"
			original-path="src/assets/images/me.jpg"
			alt="Akash's Photo"
			img-class="w-full aspect-3/2 sm:aspect-6/7 object-cover"
			class="w-full sm:w-1/3 shrink-0 rounded-lg"
		/>
		<div class="flex flex-col flex-1 min-w-0">
			<div>
				<h1 class="sm:mt-0 mb-2 text-gray-100 text-5xl">
					Hi, I'm <span class="text-amber-300">Akash</span>
				</h1>
				<h4 class="text-gray-400 mt-2 mb-8 font-light">
					I write code and wander places — sometimes together.
				</h4>
			</div>

			<p class="mb-8">
				I'm a developer at an
				<a href="https://frappe.io/" target="_blank">awesome company</a>,
				currently building an
				<a href="https://github.com/frappe/mail" target="_blank">
					open-source email client</a
				>. I built this website to maintain a digital footprint of my
				<router-link to="/places">photos</router-link> and
				<router-link to="/journal">thoughts</router-link>. This is <i>not</i> a
				portfolio, but I've listed some of my past
				<router-link to="/work">work</router-link> as well. Feel free to explore
				👋
			</p>

			<div class="border-t border-gray-400 pt-6">
				<p class="text-gray-400 text-sm mb-4 font-light">Elsewhere</p>
				<div class="flex items-center space-x-8">
					<Socials />
				</div>
			</div>
		</div>
	</div>
</template>
