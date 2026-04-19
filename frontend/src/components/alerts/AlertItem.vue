<template>
	<div class="alert-item">
		<div>Titulo</div>
		<div class="descriptors-section">
			<p class="descriptor">Hola1</p>
			<p class="descriptor">Hola2</p>
			<p class="descriptor">Hola2</p>
			<p class="descriptor">Hola2</p>
			<p class="descriptor">Hola2</p>
		</div>
		<div>Sociedad</div>
		<div>*****</div>
		<div>Correo</div>
		<div class="rss-section">
			<p class="rss">El País: www.api2.rtve.es</p>
			<p class="rss">El País: www.api2.rtve.es</p>
			<p class="rss">El País: www.api2.rtve.es</p>
			<p class="rss">El País: www.api2.rtve.es</p>
		</div>
		<div class="action-section"><button class="x-button">X</button></div>
	</div>
</template>

<script setup lang="ts"></script>

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
