<template>
	<div class="source-item">
		<div @click="toggleRssSection" class="source-section">
			<div class="source-info">
				<p class="source-name">{{ props.name }}</p>
				<p>{{ props.url }}</p>
			</div>
			<div class="source-options">
				<button
					:class="[
						'dropdown-button',
						showRssSection ? 'dropdown-button--active' : '',
					]"
				>
					V
				</button>
				<button @click.stop="deleteItem" class="x-button">X</button>
			</div>
		</div>
		<div v-if="showRssSection" class="rss-section">
			<button @click="toggleNewRss" class="form-button">
				+ NUEVO RSS
			</button>
			<NewRssItem v-if="showNewRss" />
			<div class="rss-item-container">
				<RssItem
					:id="1"
					iptcCategory="Sociedad"
					url="www.api2.rtve.es"
				/>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import NewRssItem from "./NewRssItem.vue";
import RssItem from "./RssItem.vue";

type Props = { id: number; name: string; url: string };
const props = defineProps<Props>();

const showRssSection = ref<boolean>(false);
const showNewRss = ref<boolean>(false);

const toggleRssSection = () => {
	showRssSection.value = !showRssSection.value;
};

const toggleNewRss = () => {
	showNewRss.value = !showNewRss.value;
};

const deleteItem = () => {
	console.log("ELIMINADOOO");
};
</script>

<style scoped>
.source-item {
	display: flex;
	flex-direction: column;
}

.source-section {
	cursor: pointer;
	display: flex;
	justify-content: space-between;
	align-items: center;
	border: 2px solid var(--black);
	padding-left: 1rem;
}

.source-name {
	font-weight: bold;
}

.source-options {
	display: flex;
}

.dropdown-button {
	font-size: 1.5rem;
	padding: 1rem;
}

.dropdown-button--active {
	rotate: 180deg;
}

.rss-section {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	padding: 1rem;
	border: 2px solid var(--black);
	border-top: none;
}

.form-button {
	width: max-content;
}

.rss-item-container {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	width: max-content;
}
</style>
