<template>
	<div class="new-alert-item">
		<input v-model="fields.name" type="text" name="alert-title" placeholder="TITULO..." class="title" />

		<div class="horizontal-field">
			<p>CRON:</p>
			<input v-model="fields.cron" type="text" name="alert-cron" placeholder="* * * * *" />
		</div>

		<div class="horizontal-field">
			<p>NOTIFICACIONES:</p>
			<select v-model="fields.notification" name="alert-notification-option">
				<option value="email">Correo</option>
				<option value="app">App</option>
			</select>
		</div>

		<div class="expandable-fields-container">
			<div class="vertical-field">
				<p>CATEGORÍA</p>
				<select v-model.number="fields.categoryId" name="alert-category">
					<option :value="0" disabled>Selecciona...</option>
					<option v-for="category in iptcCategories" :key="category.id" :value="category.id">
						{{ category.name }}
					</option>
				</select>

				<div class="expanded-field">
					<p>CANALES RSS</p>
					<div class="sources-container">
						<div v-for="group in channelsBySource" :key="group.source.id" class="source">
							<p>{{ group.source.name }}</p>
							<div class="rss-container">
								<label v-for="ch in group.channels" :key="ch.id" class="checkbox">
									<input
										type="checkbox"
										:value="ch.id"
										v-model="fields.channelIds"
									/>
									{{ ch.url }}
								</label>
							</div>
						</div>
						<p v-if="channelsBySource.length === 0">No hay canales disponibles.</p>
					</div>
				</div>
			</div>

			<div class="vertical-field">
				<p>DESCRIPTORES</p>
				<input
					v-model="fields.descriptorsText"
					type="text"
					name="alert-descriptors"
					placeholder="separados por coma"
				/>
				<div class="expanded-field">
					<p>DESCRIPTORES AÑADIDOS</p>
					<div>
						<p v-for="d in parsedDescriptors" :key="d" class="descriptor-chip">{{ d }}</p>
						<p v-if="parsedDescriptors.length === 0">Ninguno todavía.</p>
					</div>
				</div>
			</div>
		</div>

		<p v-if="error" class="error-msg">{{ error }}</p>
		<button :disabled="loading" @click="sendForm" class="form-button">
			{{ loading ? "CREANDO..." : "ACEPTAR" }}
		</button>
	</div>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from "vue";
import { useApiCall } from "@/api/useApiCall";
import { useAuthStore } from "@/stores/auth";
import type {
	CategoryResponse,
	InformationSourceResponse,
	RssChannelResponse,
} from "@/api/types";

type Props = {
	categories: CategoryResponse[];
	sources: InformationSourceResponse[];
	channels: RssChannelResponse[];
};
const props = defineProps<Props>();
const emit = defineEmits<{ created: [] }>();

const api = useApiCall();
const auth = useAuthStore();

const fields = reactive({
	name: "",
	cron: "* * * * *",
	notification: "email",
	categoryId: 0,
	channelIds: [] as number[],
	descriptorsText: "",
});
const loading = ref(false);
const error = ref("");

const iptcCategories = computed(() =>
	props.categories.filter((c) => /^\d{8}$/.test(c.source)),
);

const parsedDescriptors = computed(() =>
	fields.descriptorsText
		.split(",")
		.map((d) => d.trim())
		.filter((d) => d.length > 0),
);

const channelsBySource = computed(() => {
	return props.sources
		.map((source) => ({
			source,
			channels: props.channels.filter((ch) => ch.information_source_id === source.id),
		}))
		.filter((group) => group.channels.length > 0);
});

const sendForm = async () => {
	error.value = "";
	if (!fields.name.trim()) {
		error.value = "Introduce un título.";
		return;
	}
	if (!fields.cron.trim()) {
		error.value = "Introduce una expresión cron.";
		return;
	}
	if (!fields.categoryId) {
		error.value = "Selecciona una categoría.";
		return;
	}
	if (parsedDescriptors.value.length === 0) {
		error.value = "Añade al menos un descriptor.";
		return;
	}
	if (!auth.token || !auth.user) {
		error.value = "Sesión no iniciada.";
		return;
	}

	const category = iptcCategories.value.find((c) => c.id === fields.categoryId);
	if (!category) {
		error.value = "Categoría no válida.";
		return;
	}

	loading.value = true;
	try {
		await api.createUserAlert(auth.token, auth.user.id, {
			name: fields.name.trim(),
			descriptors: parsedDescriptors.value,
			categories: [{ code: category.source, label: category.name }],
			rss_channels_ids: fields.channelIds,
			information_sources_ids: [],
			cron_expression: fields.cron.trim(),
		});
		fields.name = "";
		fields.descriptorsText = "";
		fields.channelIds = [];
		fields.categoryId = 0;
		emit("created");
	} catch (e: unknown) {
		error.value = e instanceof Error ? e.message : "Error creando alerta.";
	} finally {
		loading.value = false;
	}
};
</script>

<style scoped>
.new-alert-item {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	padding: 1rem;
	border: 2px solid var(--black);
	width: 50%;
}

.title {
	font-size: 1.5rem;
}

.horizontal-field {
	display: flex;
	align-items: center;
	gap: 1ch;
}

.vertical-field {
	display: flex;
	flex-direction: column;
	gap: 0.2rem;
}

.expandable-fields-container {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 1rem;
}

.expanded-field {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	border: 1px solid var(--black);
	padding: 1rem;
}

.checkbox {
	display: flex;
	align-items: center;
	flex-direction: row;
	gap: 0.5rem;
}

.checkbox > input {
	width: max-content;
}

.sources-container {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	max-height: 240px;
	overflow-y: auto;
}

.source {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
}

.rss-container {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
}

.descriptor-chip {
	display: inline-block;
	background-color: rgb(215, 215, 215);
	padding: 0.2rem 0.5rem;
	margin: 0.2rem;
}

p {
	font-weight: bold;
}

.form-button {
	padding: 1rem;
	background-color: var(--black);
	color: white;
	width: max-content;
}

.form-button:disabled {
	opacity: 0.6;
	cursor: not-allowed;
}

.error-msg {
	color: rgb(203, 61, 61);
	border: 1px solid rgb(203, 61, 61);
	background-color: rgb(254, 236, 236);
	padding: 0.5rem;
	font-size: 0.9rem;
}
</style>
