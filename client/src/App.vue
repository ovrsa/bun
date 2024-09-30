<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import apiClient from "./services/auth";

export default {
  name: "App",
  created() {
    apiClient
      .get("csrf-token/")
      .then((response) => {})
      .catch((error) => {
        console.error("CSRFトークンの取得に失敗しました。", error);
      });
  },
};
</script>

<style></style>
