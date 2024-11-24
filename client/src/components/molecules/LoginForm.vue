<template>
  <form @submit.prevent="onSubmit" class="space-y-6">
    <h2 class="text-2xl mb-20 text-center">Login</h2>

    <InputField
      type="text"
      v-model="username"
      placeholder="Username"
      :errorMessage="errors.username ? 'Username is required.' : ''"
    />

    <InputField
      type="password"
      v-model="password"
      placeholder="Password"
      :errorMessage="errors.password ? 'Password is required.' : ''"
    />

    <Button type="submit">Log In</Button>

    <div class="text-center">
      <span class="text-sm text-gray-700">Don't have an account?</span>
      <a href="/signup" class="text-blue-600 text-sm hover:underline">
        Sign up now
      </a>
    </div>

    <div v-if="errorMessage" class="mt-4 text-red-500 text-center">
      {{ errorMessage }}
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import InputField from "@/components/atoms/InputField.vue";
import Button from "@/components/atoms/Button.vue";
import apiClient from "@/services/auth";

const username = ref("");
const password = ref("");

const errors = ref({ username: false, password: false });
const errorMessage = ref("");

const store = useStore();
const router = useRouter();

const onSubmit = async () => {
  errors.value.username = !username.value;
  errors.value.password = !password.value;

  if (!errors.value.username && !errors.value.password) {
    try {
      const response = await apiClient.post("login/", {
        username: username.value,
        password: password.value,
      });

      await store.dispatch("auth/checkAuth");
      router.push("/");
    } catch (err: unknown) {
      errorMessage.value = "ログインに失敗しました。";
      console.error(`Login failed: ${err}`);
    }
  }
};
</script>
