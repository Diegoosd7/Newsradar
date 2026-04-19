<template>
	<div class="new-alert-item">
		<input
			type="text"
			name="alert-title"
			placeholder="TITULO..."
			class="title"
		/>
		<div class="horizontal-field">
			<p>CRON:</p>
			<input type="text" name="alert-cron" placeholder="* * * * *" />
		</div>
		<div class="horizontal-field">
			<p>NOTIFICACIONES:</p>
			<select name="alert-notification-option">
				<option value="notification-by-email">Correo</option>
				<option value="notification-by-app">App</option>
			</select>
		</div>
		<div class="expandable-fields-container">
			<div class="vertical-field">
				<p>CATEGORÍA</p>
				<select name="alert-category">
					<template v-for="category in iptcCategories">
						<option :value="category">{{ category }}</option>
					</template>
				</select>
				<div class="expanded-field">
					<p>CANALES RSS</p>
					<div class="sources-container">
						<div
							v-for="(source, sourceName) in rssChannelsSociedad"
							class="source"
						>
							<p>{{ sourceName }}</p>
							<div class="rss-container">
								<template v-for="rssChannel in source">
									<label class="checkbox">
										<input
											type="checkbox"
											:name="`${rssChannel.id}`"
										/>
										{{ rssChannel.name }}
									</label>
								</template>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="vertical-field">
				<p>DESCRIPTOR</p>
				<input type="text" name="alert-cron" />
				<div class="expanded-field">
					<p>DESCRIPTORES EXTRA</p>
					<div>
						<label class="checkbox">
							<input type="checkbox" name="rss-1" />
							descriptor recomendado
						</label>
					</div>
				</div>
			</div>
		</div>
		<button class="form-button">ACEPTAR</button>
	</div>
</template>

<script setup lang="ts">
const iptcCategories = ["Sociedad", "Deportes"];

const rssChannelsSociedad = {
	"El País": [
		{ id: 1, name: "rss-1" },
		{ id: 2, name: "rss-2" },
	],
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
}

.checkbox > input {
	width: max-content;
}

.sources-container {
	display: flex;
	flex-direction: column;
	gap: 1rem;
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

p {
	font-weight: bold;
}
</style>
