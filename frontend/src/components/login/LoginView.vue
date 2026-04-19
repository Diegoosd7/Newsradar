<template>
	<div class="view">
		<div class="login-register-modal">
			<div class="options">
				<button
					@click="changeToLogin"
					:class="[
						'option',
						activeForm === 'LOGIN' ? 'option--active' : '',
					]"
				>
					LOGIN
				</button>
				<button
					@click="changeToRegister"
					:class="[
						'option',
						activeForm === 'REGISTER' ? 'option--active' : '',
					]"
				>
					REGISTRO
				</button>
			</div>
			<LoginForm v-if="activeForm === 'LOGIN'" />
			<RegisterForm v-else />
		</div>
	</div>
</template>

<script setup lang="ts">
import LoginForm from "./LoginForm.vue";
import RegisterForm from "./RegisterForm.vue";
import { ref } from "vue";

const activeForm = ref<"LOGIN" | "REGISTER">("LOGIN");

const changeToLogin = () => {
	activeForm.value = "LOGIN";
};
const changeToRegister = () => {
	activeForm.value = "REGISTER";
};
</script>

<style scoped>
.login-register-modal {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	border: 2px solid var(--black);
	width: max-content;
}

.options {
	display: grid;
	grid-template-columns: 1fr 1fr;
	width: 100%;
}

.option {
	color: white;
	background-color: var(--black);
	padding: 1rem;
	transition: 0.3s;
}

.option--active,
.option:hover {
	font-size: 1.5rem;
	color: black;
	background-color: rgb(210, 210, 247);
	background-color: rgb(255, 255, 255);
}

.form {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	padding: 1rem;
	width: 400px;
	background-color: rgb(210, 210, 247);
	background-color: rgb(255, 255, 255);
}
</style>
