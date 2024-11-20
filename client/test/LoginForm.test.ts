import LoginForm from '@/components/molecules/LoginForm.vue';
import { mount } from '@vue/test-utils';
import { createMemoryHistory, createRouter } from 'vue-router';
import { createStore } from 'vuex';

const store = createStore({
  modules: {
    auth: {
      namespaced: true,
      actions: {
        checkAuth: vi.fn(), // スパイとして設定
      },
    },
  },
});

const router = createRouter({
  history: createMemoryHistory(),
  routes: [],
});

describe('LoginForm', () => {
  it('should log in successfully', async () => {
    const wrapper = mount(LoginForm, {
      global: {
        plugins: [store, router],
      },
    });

    await wrapper.find('input[type="email"]').setValue('test@example.com');
    await wrapper.find('input[type="password"]').setValue('password');
    await wrapper.find('form').trigger('submit.prevent');

    expect(store.dispatch).toHaveBeenCalledWith('auth/checkAuth');
    expect(wrapper.text()).not.toContain('ログインに失敗しました。');
  });

  it('should show error message on login failure', async () => {
    const wrapper = mount(LoginForm, {
      global: {
        plugins: [store, router],
      },
    });

    await wrapper.find('input[type="email"]').setValue('test@example.com');
    await wrapper.find('input[type="password"]').setValue('wrongpassword');
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.text()).toContain('ログインに失敗しました。');
  });
});
