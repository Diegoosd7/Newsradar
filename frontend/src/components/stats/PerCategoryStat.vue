<template>
	<div class="per-category-stat">
		<p class="title">{{ title }}</p>

		<div v-if="items.length === 0" class="empty-state">
			Sin datos
		</div>

		<ul v-else class="items-list">
			<li v-for="item in items" :key="`${item.category_code}-${item.category_label}`" class="item-row">
				<span class="item-label">{{ item.category_label }}</span>
				<span class="item-count">{{ item.count }}</span>
			</li>
		</ul>
	</div>
</template>

<script setup lang="ts">
import type { CategoryCountItem } from "@/api/types";

type Props = {
	title: string;
	items: CategoryCountItem[];
};

defineProps<Props>();
</script>

<style scoped>
.per-category-stat {
	display: flex;
	flex-direction: column;
	border: 2px solid var(--black);
	padding: 1rem;
	gap: 1rem;
	min-height: 220px;
}

.title {
	font-weight: bold;
	margin: 0;
}

.empty-state {
	color: #666;
}

.items-list {
	list-style: none;
	padding: 0;
	margin: 0;
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
}

.item-row {
	display: flex;
	justify-content: space-between;
	align-items: center;
	border-bottom: 1px solid #ddd;
	padding-bottom: 0.35rem;
}

.item-label {
	font-size: 0.95rem;
}

.item-count {
	font-weight: bold;
}
</style>