module.exports = [
  {
    files: ["**/*.{js,ts,vue}"],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: "module",
      parser: require("@typescript-eslint/parser"),
      globals: {
        document: "readonly",
        navigator: "readonly",
        window: "readonly",
      },
    },
    plugins: {
      vue: require("eslint-plugin-vue"),
      "@typescript-eslint": require("@typescript-eslint/eslint-plugin"),
    },
    rules: {
      ...require("eslint-plugin-vue").configs["vue3-recommended"].rules,
      ...require("@typescript-eslint/eslint-plugin").configs.recommended.rules,
      "semi": "error",
      "quotes": ["error", "double"],
    },
  },
];
