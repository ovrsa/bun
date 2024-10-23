<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="outline" size="icon" class="rounded-full">
        <img
          src="/img/user_icon.png"
          width="30"
          height="30"
          alt="Avatar"
          class="overflow-hidden rounded-full"
        />
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent class="w-56">
      <DropdownMenuLabel>Account</DropdownMenuLabel>
      <DropdownMenuSeparator />
      <DropdownMenuCheckboxItem v-model="Profile" class="menu-item" disabled>
        Profile
      </DropdownMenuCheckboxItem>
      <DropdownMenuCheckboxItem v-model="Setting" class="menu-item" disabled>
        Setting
      </DropdownMenuCheckboxItem>
      <DropdownMenuCheckboxItem @click="$emit('logout')" class="menu-item">
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
} from "../ui/dropdown-menu";

const Profile = ref(false);
const Setting = ref(false);
</script>

<style scoped>
.menu-item {
  cursor: pointer;
}
</style>
