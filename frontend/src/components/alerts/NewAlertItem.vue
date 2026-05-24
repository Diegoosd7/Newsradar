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
				<div class="descriptor-input-row">
					<input
						v-model="fields.descriptorsText"
						type="text"
						name="alert-descriptors"
						placeholder="separados por coma"
					/>
					<button
						:disabled="suggestLoading || parsedDescriptors.length === 0"
						@click="suggestKeywords"
						class="suggest-button"
					>
						{{ suggestLoading ? "..." : "SUGERIR" }}
					</button>
				</div>

				<div v-if="suggestions.length > 0" class="expanded-field suggestions-field">
					<p>SUGERENCIAS <span class="hint">(clic para añadir)</span></p>
					<div class="chips-row">
						<span
							v-for="s in suggestions"
							:key="s"
							class="suggestion-chip"
							@click="addSuggestion(s)"
						>
							+ {{ s }}
						</span>
					</div>
					<p v-if="suggestError" class="suggest-error">{{ suggestError }}</p>
				</div>
				<p v-if="suggestError && suggestions.length === 0" class="suggest-error">{{ suggestError }}</p>

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

const suggestions = ref<string[]>([]);
const suggestLoading = ref(false);
const suggestError = ref("");

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

const suggestKeywords = async () => {
	if (!auth.token || !auth.user) return;
	suggestLoading.value = true;
	suggestError.value = "";
	suggestions.value = [];
	try {
		console.log("Token:", auth.token);
		console.log("Body enviado:", JSON.stringify({ keyword: parsedDescriptors.value[0] }));
		const res = await fetch(`/api/v1/users/suggest-keywords`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${auth.token}`,
			},
			body: JSON.stringify({ keyword: parsedDescriptors.value[0] }),
		});
		if (!res.ok) throw new Error(`Error ${res.status}`);
		const data = await res.json();
		// El endpoint puede devolver { suggestions: [...] } o directamente un array
		const raw: string[] = Array.isArray(data) ? data : (data.suggestions ?? data.keywords ?? []);
		// Filtrar los que ya están como descriptores
		suggestions.value = raw.filter(
			(s) => !parsedDescriptors.value.map((d) => d.toLowerCase()).includes(s.toLowerCase())
		);
		if (suggestions.value.length === 0) {
			suggestError.value = "No se encontraron sugerencias nuevas.";
		}
	} catch (e: unknown) {
		suggestError.value = e instanceof Error ? e.message : "Error obteniendo sugerencias.";
	} finally {
		suggestLoading.value = false;
	}
};

const addSuggestion = (s: string) => {
	const current = parsedDescriptors.value;
	if (!current.map((d) => d.toLowerCase()).includes(s.toLowerCase())) {
		fields.descriptorsText = [...current, s].join(", ");
	}
	suggestions.value = suggestions.value.filter((x) => x !== s);
};

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
		suggestions.value = [];
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

.descriptor-input-row {
	display: flex;
	gap: 0.5rem;
	align-items: center;
}

.descriptor-input-row input {
	flex: 1;
}

.suggest-button {
	padding: 0.4rem 0.8rem;
	background-color: var(--black);
	color: white;
	font-weight: bold;
	font-size: 0.8rem;
	white-space: nowrap;
}

.suggest-button:disabled {
	opacity: 0.5;
	cursor: not-allowed;
}

.suggestions-field {
	margin-top: 0.3rem;
}

.hint {
	font-size: 0.75rem;
	font-weight: normal;
	color: #666;
}

.chips-row {
	display: flex;
	flex-wrap: wrap;
	gap: 0.4rem;
}

.suggestion-chip {
	background-color: #d7f0d7;
	border: 1px solid #5a9e5a;
	padding: 0.2rem 0.6rem;
	cursor: pointer;
	font-size: 0.85rem;
	font-weight: normal;
}

.suggestion-chip:hover {
	background-color: #b3e0b3;
}

.suggest-error {
	color: rgb(150, 60, 60);
	font-size: 0.85rem;
	font-weight: normal;
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