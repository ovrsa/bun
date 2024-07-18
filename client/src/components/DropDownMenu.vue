<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="outline" size="icon" class="rounded-full">
        <img
          src="/user_icon.png"
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
      <DropdownMenuCheckboxItem v-model="Profile">
        Profile
      </DropdownMenuCheckboxItem>
      <DropdownMenuCheckboxItem v-model="Setting" disabled>
        Setting
      </DropdownMenuCheckboxItem>
      <DropdownMenuCheckboxItem v-model="Logout">
        Logout
      </DropdownMenuCheckboxItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>

<script setup lang="ts">
import { ref, defineExpose } from 'vue';
import { Button } from '../components/ui/button';
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '../components/ui/dropdown-menu';

const Profile = ref(true);
const Setting = ref(false);
const Logout = ref(false);

defineExpose({
  Profile,
  Setting,
  Logout,
});
</script>

<style scoped></style>
