<template>
	<div class="view">
		<div class="header">
			<h1>Estadísticas</h1>
		</div>
		<div class="main">
			<div class="total-number-container">
				<template v-for="stat in totalNumberStats">
					<TotalNumberStat v-bind="stat" />
				</template>
			</div>
			<div class="per-category-container">
				<template v-for="stat in perCategoryStats">
					<PerCategoryStat v-bind="stat" />
				</template>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import PerCategoryStat from "./PerCategoryStat.vue";
import TotalNumberStat from "./TotalNumberStat.vue";
import { onMounted, ref } from "vue";

const totalNumberStats = ref([
	{ title: "FUENTES", number: 0 },
	{ title: "RSS", number: 0 },
	{ title: "NOTICIAS", number: 0 },
	{ title: "ALERTAS", number: 0 },
]);
const perCategoryStats = ref([
	{ title: "NOTICIAS POR CATEGORÍA" },
	{ title: "ALERTAS POR CATEGORÍA" },
]);

const getTotalStats = () => {
	const fuentesNum = 10;
	const rssNum = 10;
	const noticiasNum = 10;
	const alertasNum = 10;

	totalNumberStats.value = [
		{ title: "FUENTES", number: fuentesNum },
		{ title: "RSS", number: rssNum },
		{ title: "NOTICIAS", number: noticiasNum },
		{ title: "ALERTAS", number: alertasNum },
	];
};

const getPerCategoryStats = () => {
	perCategoryStats.value = [
		{ title: "NOTICIAS POR CATEGORÍA" },
		{ title: "ALERTAS POR CATEGORÍA" },
	];
};

onMounted(() => {
	getTotalStats();
	getPerCategoryStats();
});
</script>

<style scoped>
.view,
.main {
	display: flex;
	flex-direction: column;
	gap: 1rem;
}

.total-number-container {
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	gap: 1rem;
}

.per-category-container {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 1rem;
}
</style>
