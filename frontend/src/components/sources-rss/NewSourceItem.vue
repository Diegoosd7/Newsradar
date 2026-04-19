<template>
	<div class="new-source-item">
		<input class="field" type="text" name="url" placeholder="Nombre..." />
		<input class="field" type="text" name="url" placeholder="URL..." />
		<button class="add-button">+</button>
	</div>
</template>

<script setup lang="ts"></script>

<style scoped>
.new-source-item {
	display: flex;
	gap: 1rem;
	border: 2px solid var(--black);
	padding: 1rem;
}

.add-button {
	font-size: 1.5rem;
}

.add-button:hover {
	color: green;
}
</style>
