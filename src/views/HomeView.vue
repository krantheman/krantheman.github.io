<template>
	<div class="flex items-center sm:items-start flex-col sm:flex-row sm:py-16">
		<img
			src="@/assets/images/me.avif"
			alt="Akash's Photo"
			class="shrink-0 sm:aspect-square sm:w-1/3 object-cover rounded-md"
		/>
		<div class="sm:ml-8">
			<h1 class="sm:mt-0">Hi, I'm Akash</h1>
			<p>I like programming and travelling—sometimes together!</p>
			<p>
				I work as a software developer at an
				<a href="https://frappe.io/" target="_blank">awesome company</a>, where
				I'm currently building an
				<a href="https://github.com/frappe/mail" target="_blank">
					open-source email client</a
				>.
			</p>
			<p>
				I made this website primarily out of my disdain for Instagram and how it
				handled
				<router-link to="/gallery">my images</router-link>. I figured I could
				also use it for <router-link to="/blog">writing stuff</router-link> now
				and then. This is <i>not</i> a portfolio, but I've listed some of
				<router-link to="/projects">my projects</router-link>
				as well.
			</p>
			<p>
				You can find links to all my socials in the navbar. Feel free to reach
				out for anything!
			</p>
		</div>
	</div>
</template>
