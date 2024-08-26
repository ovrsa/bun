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
import { ref } from 'vue';
import { useRouter } from 'vue-router';
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

const router = useRouter();

const handleLogout = () => {
  // ログインページに遷移
  router.push('/login');
};
</script>

<style scoped>
.menu-item {
  cursor: pointer;
}
</style>
