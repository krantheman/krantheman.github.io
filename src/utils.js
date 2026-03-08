export const getDate = (date) => {
	const [year, month] = date.split("-");
	const monthNames = [
		"Jan",
		"Feb",
		"Mar",
		"Apr",
		"May",
		"Jun",
		"Jul",
		"Aug",
		"Sep",
		"Oct",
		"Nov",
		"Dec",
	];

	const monthIndex = parseInt(month, 10) - 1;
	return `${monthNames[monthIndex]} 20${year}`;
};
