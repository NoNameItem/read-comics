import antfu from "@antfu/eslint-config"

export default antfu({
  // Enable stylistic formatting rules
  // stylistic: true,

  // Or customize the stylistic rules
  stylistic: {
    indent: 2, // 4, or 'tab'
    quotes: "double", // or 'double'
  },

  // TypeScript and Vue are auto-detected, you can also explicitly enable them:
  typescript: true,
  vue:        true,

  // Disable jsonc and yaml support
  jsonc: false,
  yaml:  false,

  ignores: [
    "./fixtures",
    "./nuxt",
    "./node_modules",
    "dist",
    "*.d.ts",
    "@core",
    "@layouts",
  ],
}, { rules: {
  "antfu/top-level-function": ["off"],
  "style/key-spacing":        ["error", {
    singleLine: {
      beforeColon: false,
      afterColon:  true,
    },
    multiLine: {
      beforeColon: false,
      afterColon:  true,
      align:       "value",
    },
  }],
  "style/type-annotation-spacing": ["error", { before: false, after: true }],
  "style/no-multi-spaces":         ["off"],
  "node/prefer-global/process":    ["off"],
} })
