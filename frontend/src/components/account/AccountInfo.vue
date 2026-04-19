<template>
	<div class="account-info">
		<p class="title">INFORMACIÓN DE LA CUENTA</p>
		<div class="role-section">
			<p class="role">
				ROL: <span class="highlight">{{ auth.role }}</span>
			</p>
			<p class="admin-callout">
				Para cambiar de rol, contacta con tu administrador.
			</p>
		</div>
		<div class="verification-section">
			<p v-if="auth.user?.is_verified" class="verify-tag">CUENTA VERIFICADA</p>
			<template v-else>
				<p>Tu cuenta aún no está verificada. Revisa tu bandeja de entrada.</p>
			</template>
		</div>
	</div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<style scoped>
.account-info {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	border: 2px solid var(--black);
	padding: 1rem;
	width: 50%;
}

.title {
	font-size: 1.2rem;
	font-weight: bold;
	text-align: center;
}

.verify-tag {
	display: flex;
	justify-content: center;
	padding: 1rem;
	color: green;
	border: 1px solid green;
	background-color: #d5f1d5;
}

.role {
	display: flex;
	align-items: center;
	gap: 1ch;
}

.highlight {
	border: 1px solid var(--black);
	padding: 0 0.3rem;
}

.admin-callout {
	display: flex;
	color: var(--black);
	border: 1px solid var(--black);
	background-color: rgb(215, 215, 215);
	padding: 1rem;
}

.role-section {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
}
</style>
