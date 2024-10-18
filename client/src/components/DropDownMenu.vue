<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="outline" size="icon" class="rounded-full">
        <img
          src=".../public/img/user_icon.png"
          width="25"
          height="25"
          alt="Avatar"
          class="overflow-hidden rounded-full"
        />
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent class="w-56">
      <DropdownMenuLabel>My Account</DropdownMenuLabel>
      <DropdownMenuSeparator />
      <DropdownMenuCheckboxItem v-model="Profile" class="menu-item">
        Profile
      </DropdownMenuCheckboxItem>
      <DropdownMenuCheckboxItem v-model="Setting" class="menu-item" disabled>
        Setting
      </DropdownMenuCheckboxItem>
      <DropdownMenuCheckboxItem @click="handleLogout" class="menu-item">
        Logout
      </DropdownMenuCheckboxItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>

<script setup lang="ts">
import { ref } from "vue";
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "../components/ui/dropdown-menu";
import { useStore } from "vuex";

const Profile = ref(true);
const Setting = ref(false);
const store = useStore();

const handleLogout = () => {
  store.dispatch("auth/logout");
};
</script>

<style scoped>
.menu-item {
  cursor: pointer;
}
</style>
