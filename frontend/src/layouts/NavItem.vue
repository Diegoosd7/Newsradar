<template>
	<RouterLink
		:to="props.link"
		:class="[
			'nav-item',
			isActiveLink(`${props.link}`) ? 'nav-item--active' : '',
		]"
		>{{ props.name }}
	</RouterLink>
</template>

<script setup lang="ts">
import { RouterLink, useRoute } from "vue-router";

type Props = { link: string; name: string };
const props = defineProps<Props>();

const isActiveLink = (routePath: string) => {
	const route = useRoute();
	return route.path === routePath;
};
</script>

<style scoped>
.nav-item {
	padding: 1rem;
	color: white;
	white-space: nowrap;
}

.nav-item--active,
.nav-item:hover {
	background-color: rgb(49, 49, 78);
}
</style>
