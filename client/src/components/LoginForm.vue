<template>
  <form @submit.prevent="onSubmit" class="space-y-6">
    <h2 class="text-2xl mb-20 text-center">Login</h2>

    <!-- email -->
    <div class="space-y-1">
      <input
        type="email"
        v-model="email"
        class="w-full p-2 border border-gray-300 rounded-lg bg-white bg-opacity-50 placeholder-gray-400"
        placeholder="Email"
      />
      <p v-if="errors.email" class="text-red-500 text-xs">Email is required.</p>
    </div>

    <!-- password -->
    <div class="space-y-1">
      <input
        id="password"
        type="password"
        v-model="password"
        class="w-full p-2 border border-gray-300 rounded-lg bg-white bg-opacity-50 placeholder-gray-400"
        placeholder="Password"
      />
      <p v-if="errors.password" class="text-red-500 text-xs">
        Password is required.
      </p>
    </div>

    <div class="text-center pt-5">
      <a href="" class="text-blue-600 text-sm hover:underline">
        Forgot your password?
      </a>
    </div>

    <!-- Submit -->
    <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded-lg">
      Log In
    </button>

    <div class="text-center">
      <span class="text-sm text-gray-700">Don't have an account?</span>
      <a href="/signup" class="text-blue-600 text-sm hover:underline">
        Sign up now
      </a>
    </div>

    <div v-if="message" class="mt-4 text-green-500 text-center">
      {{ message }}
    </div>
    <div v-if="errorMessage" class="mt-4 text-red-500 text-center">
      {{ errorMessage }}
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import apiClient from '../plugins/axios';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import type { AxiosError } from 'axios';

const email = ref('');
const password = ref('');
const errors = ref({ email: false, password: false });
const message = ref('');
const errorMessage = ref('');

const store = useStore();
const router = useRouter();

const onSubmit = async () => {
  if (!email.value) {
    errors.value.email = true;
  } else {
    errors.value.email = false;
  }

  if (!password.value) {
    errors.value.password = true;
  } else {
    errors.value.password = false;
  }

  if (!errors.value.email && !errors.value.password) {
    try {
      const response = await apiClient.post('login/', {
        email: email.value,
        password: password.value,
      });
      message.value = response.data.message;
      await store.dispatch('checkAuth');
      router.push('/');
      console.log(`Login success: ${response.data.message}`);
    } catch (err: unknown) {
      const error = err as AxiosError;
      if (error.response && error.response.data) {
        errorMessage.value = Object.values(error.response.data)
          .flat()
          .join(' ');
      } else {
        errorMessage.value = 'ログインに失敗しました。';
      }
    }
  }
};
</script>

<style scoped></style>
