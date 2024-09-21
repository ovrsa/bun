<template>
  <form @submit.prevent="onSubmit" class="space-y-6">
    <h2 class="text-2xl mb-20 text-center">Create Account</h2>

    <!-- username -->
    <div class="space-y-1">
      <input
        id="username"
        type="text"
        v-model="user.username"
        class="w-full p-2 border border-gray-300 rounded-lg bg-white bg-opacity-50 placeholder-gray-400"
        placeholder="UserName"
        required
      />
      <p v-if="errors.username" class="text-red-500 text-xs">
        UserName is required.
      </p>
    </div>

    <!-- email -->
    <div class="space-y-1">
      <input
        id="email"
        type="email"
        v-model="user.email"
        class="w-full p-2 border border-gray-300 rounded-lg bg-white bg-opacity-50 placeholder-gray-400"
        placeholder="Email"
        required
      />
      <p v-if="errors.email" class="text-red-500 text-xs">Email is required.</p>
    </div>

    <!-- password -->
    <div class="space-y-1">
      <input
        id="password"
        type="password"
        v-model="user.password"
        class="w-full p-2 border border-gray-300 rounded-lg bg-white bg-opacity-50 placeholder-gray-400"
        placeholder="Password"
        required
      />
      <p v-if="errors.password" class="text-red-500 text-xs">
        Password is required.
      </p>
    </div>

    <!-- password確認 -->
    <div class="space-y-1 pb-10">
      <input
        id="password_confirm"
        type="password"
        v-model="user.password_confirm"
        class="w-full p-2 border border-gray-300 rounded-lg bg-white bg-opacity-50 placeholder-gray-400"
        placeholder="Confirm Password"
        required
      />
      <p v-if="errors.password_confirm" class="text-red-500 text-xs">
        Password confirmation is required.
      </p>
    </div>

    <!-- Submit -->
    <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded-lg">
      Create Account
    </button>

    <div class="text-center">
      <span class="text-sm text-gray-700">Already have an account?</span>
      <a href="/login" class="text-blue-600 text-sm hover:underline"
        >Login now</a
      >
    </div>

    <!-- メッセージ表示 -->
    <Alert v-if="message" class="mt-4">
      <RocketIcon class="h-4 w-4 text-green-600" />
      <AlertTitle>Success!</AlertTitle>
      <AlertDescription>
        {{ message }}
      </AlertDescription>
    </Alert>

    <Alert v-if="errorMessage" class="mt-4" variant="destructive">
      <RocketIcon class="h-4 w-4 text-red-600" />
      <AlertTitle>Error!</AlertTitle>
      <AlertDescription>
        {{ errorMessage }}
      </AlertDescription>
    </Alert>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import apiClient from '../plugins/axios';
import { RocketIcon } from '@radix-icons/vue';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import type { AxiosError } from 'axios';

const user = ref({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
});

const message = ref('');
const errorMessage = ref('');
const errors = ref({
  username: false,
  email: false,
  password: false,
  password_confirm: false,
});

const onSubmit = async () => {
  errors.value.username = !user.value.username;
  errors.value.email = !user.value.email;
  errors.value.password = !user.value.password;
  errors.value.password_confirm = !user.value.password_confirm;

  if (
    !errors.value.username &&
    !errors.value.email &&
    !errors.value.password &&
    !errors.value.password_confirm
  ) {
    try {
      const response = await apiClient.post('register/', user.value);
      message.value = response.data.message;
      errorMessage.value = '';
      user.value.username = '';
      user.value.email = '';
      user.value.password = '';
      user.value.password_confirm = '';
    } catch (err: unknown) {
      const error = err as AxiosError;
      if (error.response && error.response.data) {
        const responseData = error.response.data as { [key: string]: string[] };
        errorMessage.value = Object.values(responseData).flat().join(' ');
      } else {
        errorMessage.value = '登録に失敗しました。';
      }
    }
  }
};
</script>
<style scoped></style>
