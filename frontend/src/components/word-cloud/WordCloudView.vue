<template>
	<div class="view">
		<div class="header">
			<h1>Nube de palabras</h1>
		</div>
		<div class="container">
			<template v-for="item in items">
				<WordCloudItem v-bind="item" />
			</template>
		</div>
	</div>
</template>

<script setup lang="ts">
import WordCloudItem from "./WordCloudItem.vue";
import { ref } from "vue";

const items = ref([
	{ title: "CATEGORÍA 1" },
	{ title: "CATEGORÍA 2" },
	{ title: "CATEGORÍA 3" },
]);
</script>

<style scoped>
.container {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 1rem;
}
</style>
