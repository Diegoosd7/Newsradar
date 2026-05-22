<template>
	<div class="alert-item">
		<div>{{ props.alert.name }}</div>
		<div class="descriptors-section">
			<p v-for="descriptor in props.alert.descriptors" :key="descriptor" class="descriptor">
				{{ descriptor }}
			</p>
		</div>
		<div>
			<span v-for="cat in props.alert.categories" :key="cat.code">{{ cat.label }}</span>
			<span v-if="props.alert.categories.length === 0">—</span>
		</div>
		<div>{{ props.alert.cron_expression }}</div>
		<div>Correo</div>
		<div class="rss-section">
			<p v-for="channelId in props.alert.rss_channels_ids" :key="channelId" class="rss">
				{{ channelLabel(channelId) }}
			</p>
			<p v-if="props.alert.rss_channels_ids.length === 0" class="rss">—</p>
		</div>
		<div class="action-section">
			<button @click="deleteAlert" class="x-button">X</button>
		</div>
	</div>
</template>

<script setup lang="ts">
import { useApiCall } from "@/api/useApiCall";
import { useAuthStore } from "@/stores/auth";
import type {
	AlertResponse,
	InformationSourceResponse,
	RssChannelResponse,
} from "@/api/types";

type Props = {
	alert: AlertResponse;
	channels: RssChannelResponse[];
	sources: InformationSourceResponse[];
};
const props = defineProps<Props>();
const emit = defineEmits<{ deleted: [] }>();

const api = useApiCall();
const auth = useAuthStore();

const channelLabel = (channelId: number): string => {
	const channel = props.channels.find((c) => c.id === channelId);
	if (!channel) return `#${channelId}`;
	const source = props.sources.find((s) => s.id === channel.information_source_id);
	const sourceName = source ? source.name : `Fuente #${channel.information_source_id}`;
	return `${sourceName}: ${channel.url}`;
};

const deleteAlert = async () => {
	if (!auth.token || !auth.user) return;
	if (!confirm(`¿Eliminar la alerta "${props.alert.name}"?`)) return;
	try {
		await api.deleteUserAlert(auth.token, auth.user.id, props.alert.id);
		emit("deleted");
	} catch (e: unknown) {
		alert(e instanceof Error ? e.message : "Error eliminando la alerta.");
	}
};
</script>

<style scoped>
.alert-item {
	display: grid;
	grid-template-columns: repeat(7, 150px);
	word-break: break-all;
	gap: 0.5rem;
	text-align: center;
	align-items: center;
	border: 2px solid var(--black);
	border-top: none;
	width: max-content;
}

.descriptors-section,
.rss-section {
	display: flex;
	flex-wrap: wrap;
	justify-content: center;
	padding: 1rem 0;
	gap: 1rem;
}

.descriptor,
.rss {
	background-color: rgb(215, 215, 215);
	padding: 0.2rem 0.5rem;
	word-break: keep-all;
}

.action-section {
	display: flex;
	justify-content: center;
}
</style>
