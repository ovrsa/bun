<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import apiClient from "@/application/services/auth";
import { getCookie } from "@/application/services/auth";

export default {
  name: "App",
  created() {
    apiClient
      .get("csrf-token/", { withCredentials: true })
      .then(() => {
        const csrfToken = getCookie("csrftoken");
        if (csrfToken) {
          apiClient.defaults.headers.common["X-CSRFToken"] = csrfToken;
        }
      })
      .catch((error) => {
        console.error("CSRFトークンの取得に失敗しました。", error);
      });
  },
};
</script>
