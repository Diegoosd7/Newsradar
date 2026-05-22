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
			<NewRssItem
				v-if="showNewRss"
				:source-id="props.id"
				:categories="props.categories"
				@created="onRssCreated"
			/>
			<p v-if="error" class="error-msg">{{ error }}</p>
			<p v-if="loadingChannels">Cargando canales...</p>
			<p v-else-if="channels.length === 0">Sin canales RSS asociados.</p>
			<div class="rss-item-container">
				<RssItem
					v-for="channel in channels"
					:key="channel.id"
					:id="channel.id"
					:source-id="props.id"
					:iptc-category="categoryNameById(channel.category_id)"
					:url="channel.url"
					@deleted="loadChannels"
				/>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import NewRssItem from "./NewRssItem.vue";
import RssItem from "./RssItem.vue";
import { useApiCall } from "@/api/useApiCall";
import { useAuthStore } from "@/stores/auth";
import type { CategoryResponse, RssChannelResponse } from "@/api/types";

type Props = {
	id: number;
	name: string;
	url: string;
	categories: CategoryResponse[];
};
const props = defineProps<Props>();
const emit = defineEmits<{ deleted: [] }>();

const api = useApiCall();
const auth = useAuthStore();

const showRssSection = ref<boolean>(false);
const showNewRss = ref<boolean>(false);
const channels = ref<RssChannelResponse[]>([]);
const loadingChannels = ref<boolean>(false);
const error = ref<string>("");

const categoryNameById = (categoryId: number): string => {
	const cat = props.categories.find((c) => c.id === categoryId);
	return cat ? cat.name : String(categoryId);
};

const loadChannels = async () => {
	if (!auth.token) return;
	loadingChannels.value = true;
	error.value = "";
	try {
		channels.value = await api.getSourceChannels(auth.token, props.id);
	} catch (e: unknown) {
		error.value = e instanceof Error ? e.message : "Error cargando canales.";
	} finally {
		loadingChannels.value = false;
	}
};

const toggleRssSection = async () => {
	showRssSection.value = !showRssSection.value;
	if (showRssSection.value) {
		await loadChannels();
	}
};

const toggleNewRss = () => {
	showNewRss.value = !showNewRss.value;
};

const onRssCreated = async () => {
	showNewRss.value = false;
	await loadChannels();
};

const deleteItem = async () => {
	if (!auth.token) return;
	if (!confirm(`¿Eliminar la fuente "${props.name}"?`)) return;
	try {
		await api.deleteSource(auth.token, props.id);
		emit("deleted");
	} catch (e: unknown) {
		error.value = e instanceof Error ? e.message : "Error eliminando fuente.";
	}
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
	width: 100%;
}

.error-msg {
	color: rgb(203, 61, 61);
	border: 1px solid rgb(203, 61, 61);
	background-color: rgb(254, 236, 236);
	padding: 0.5rem;
	font-size: 0.9rem;
}
</style>
