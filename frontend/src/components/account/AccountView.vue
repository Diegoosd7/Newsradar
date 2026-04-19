<template>
	<div class="view">
		<div class="header">
			<h1>Cuenta</h1>
		</div>
		<div class="main">
			<PersonalInfo />
			<AccountInfo />
		</div>
	</div>
</template>

<script setup lang="ts">
import AccountInfo from "./AccountInfo.vue";
import PersonalInfo from "./PersonalInfo.vue";
</script>

<style scoped>
.main {
	/* display: grid;
	grid-template-columns: repeat(2, 1fr); */
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	gap: 1rem;
}
</style>
