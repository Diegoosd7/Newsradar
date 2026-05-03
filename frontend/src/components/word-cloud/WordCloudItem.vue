<template>
  <div class="word-cloud-item">
    <p class="title">{{ title }}</p>

    <div v-if="words.length === 0" class="empty-state">
      Sin palabras disponibles
    </div>

    <div v-else class="words-container">
      <span
        v-for="word in words"
        :key="word.text"
        class="word"
        :style="{ fontSize: getFontSize(word.value) }"
      >
        {{ word.text }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TrendingWordItem } from "@/api/types";

type Props = {
  title: string;
  words: TrendingWordItem[];
};

const props = defineProps<Props>();

const getFontSize = (value: number) => {
  const min = 0.9;
  const max = 2;
  const scaled = Math.min(max, min + value * 0.08);
  return `${scaled}rem`;
};
</script>

<style scoped>
.word-cloud-item {
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

.words-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem 0.9rem;
  align-items: center;
}

.word {
  line-height: 1.1;
}
</style>
