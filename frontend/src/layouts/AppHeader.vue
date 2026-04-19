<template>
	<header>
		<h1 class="title">NEWSRADAR</h1>
		<div class="language">
			<button>ES</button>
			|
			<button>EN</button>
		</div>
	</header>
</template>

<script setup lang="ts"></script>

<style scoped>
header {
	--pad: 1rem;
	background-color: var(--black);
	color: white;
	padding: var(--pad);
	display: flex;
	place-content: center;
	place-items: center;
}

.title {
	color: white;
	font-weight: bold;
}

.language {
	display: flex;
	gap: 1ch;
	place-content: center;
	place-items: center;
	position: absolute;
	right: var(--pad);
}

.language > button {
	color: white;
}
</style>
