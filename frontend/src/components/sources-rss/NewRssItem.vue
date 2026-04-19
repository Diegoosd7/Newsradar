<template>
	<div class="new-rss-item">
		<select name="iptc-category">
			<template v-for="iptc in iptcCategories">
				<option :value="iptc">{{ iptc }}</option>
			</template>
		</select>
		<input class="url-field" type="text" name="url" placeholder="URL..." />
		<button class="add-button">+</button>
	</div>
</template>

<script setup lang="ts">
const iptcCategories = ["Sociedad", "Deportes"];
</script>

<style scoped>
.new-rss-item {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	border: 1px solid black;
	padding-left: 1rem;
}

.add-button {
	font-size: 1.5rem;
	padding: 1rem;
}

.add-button:hover {
	color: green;
}
</style>
