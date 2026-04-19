<template>
	<div class="view">
		<div class="header">
			<h1>Fuentes y RSS</h1>
		</div>
		<div class="main">
			<div>
				<button @click="toggleNewSource" class="form-button">
					+ NUEVA FUENTE
				</button>
			</div>
			<NewSourceItem v-if="showNewSource" />
			<div class="container">
				<!-- <template> -->
				<SourceItem :id="1" , name="El País" url="www.elpais.es" />
				<SourceItem :id="1" , name="El País" url="www.elpais.es" />
				<SourceItem :id="1" , name="El País" url="www.elpais.es" />
				<SourceItem :id="1" , name="El País" url="www.elpais.es" />
				<SourceItem :id="1" , name="El País" url="www.elpais.es" />
				<!-- </template> -->
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import NewSourceItem from "./NewSourceItem.vue";
import SourceItem from "./SourceItem.vue";
import { ref } from "vue";

const showNewSource = ref<boolean>(false);

const toggleNewSource = () => {
	showNewSource.value = !showNewSource.value;
};
</script>

<style scoped>
.main {
	display: flex;
	flex-direction: column;
	gap: 1rem;
}

.container {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 1rem;
}

.form-button {
	width: max-content;
}
</style>
