<script setup>
const WORK = [
	{
		title: "Frappe Mail",
		date: "Nov 2024 - Present",
		description: "End-to-end email management platform",
		link: "https://github.com/frappe/mail",
	},
	{
		title: "Frappe HR",
		date: "Aug 2023 - Dec 2024",
		description: "Open-source, modern, and easy-to-use HR and payroll software",
		link: "https://github.com/frappe/hrms",
	},
	{
		title: "Frappe Drive",
		date: "Jul 2022 - Mar 2023",
		description: "Open-source file storage, sharing, and collaboration",
		link: "https://github.com/frappe/drive",
	},
	{
		title: "FitPose 2",
		date: "Jan 2022 - May 2022",
		description: "Same shit but more sensibly done",
		link: "https://github.com/ABCSquad/fitpose",
	},
	{
		title: "FitPose",
		date: "Mar 2021 - May 2021",
		description:
			"Fitness web app that estimates and corrects posture using deep learning algorithms",
		link: "https://github.com/ABCSquad/FitPose-Django",
	},
	{
		title: "FarmHub",
		date: "Oct 2020 - Nov 2020",
		description: "I'm sorry about this one",
		link: "https://github.com/krantheman/Farmhub",
	},
];
</script>

<template>
	<div class="space-y-8">
		<div v-for="project in WORK" class="cursor-pointer">
			<a class="space-y-1 no-underline!" :href="project.link" target="_blank">
				<h4>{{ project.title }}</h4>
				<h6>{{ project.date }}</h6>
				<p class="text-gray-200">{{ project.description }}</p>
			</a>
		</div>
	</div>
</template>
