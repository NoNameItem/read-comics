import antfu from "@antfu/eslint-config"

export default antfu({
  formatters: {
    /**
     * Format CSS, LESS, SCSS files, also the `<style>` blocks in Vue
     * By default uses Prettier
     */
    css:      true,
    /**
     * Format HTML files
     * By default uses Prettier
     */
    html:     true,
    /**
     * Format Markdown files
     * Supports Prettier and dprint
     * By default uses Prettier
     */
    markdown: false,
  },

  ignores: [
    "./fixtures",
    "./nuxt",
    "./node_modules",
    "dist",
    "*.d.ts",
    "@core",
    "@layouts",
  ],

  // Disable jsonc and yaml support
  jsonc: false,

  // Or customize the stylistic rules
  stylistic: {
    indent: 2, // 4, or 'tab'
    quotes: "double", // or 'double'
  },

  // TypeScript and Vue are auto-detected, you can also explicitly enable them:
  typescript: true,
  vue:        true,

  yaml: false,
}, {
  rules: {
    "antfu/top-level-function":        ["off"],
    "camelcase":                       ["error"],
    "consistent-return":               ["error"],
    "curly":                           ["error", "all"],
    "import/newline-after-import":     ["off"],
    "import/order":                    ["off"],
    "node/prefer-global/process":      ["off"],
    "perfectionist/sort-classes":      ["error"],
    "perfectionist/sort-enums":        ["error"],
    "perfectionist/sort-imports":      ["error"],
    "perfectionist/sort-interfaces":   ["error"],
    "perfectionist/sort-object-types": ["error"],
    "perfectionist/sort-objects":      ["error"],
    "sort-imports":                    ["off"],
    "sort-keys":                       ["off"],
    "style/array-bracket-newline":     ["error", { minItems: 5, multiline: true }],
    "style/key-spacing":               [
      "error",
      {
        multiLine: {
          afterColon:  true,
          align:       "value",
          beforeColon: false,
        },
        singleLine: {
          afterColon:  true,
          beforeColon: false,
        },
      },
    ],
    "style/no-multi-spaces":                        ["off"],
    "style/object-curly-newline":                   ["error", { multiline: true }],
    "style/type-annotation-spacing":                ["error", { after: true, before: false }],
    "ts/array-type":                                ["error"],
    // "ts/explicit-function-return-type":             ["error"],
    "ts/explicit-member-accessibility":             ["error"],
    "unicorn/better-regex":                         ["error"],
    "unicorn/prefer-array-find":                    ["error"],
    "unicorn/prefer-array-flat":                    ["error"],
    "unicorn/prefer-array-flat-map":                ["error"],
    "unicorn/prefer-array-index-of":                ["error"],
    "unicorn/prefer-array-some":                    ["error"],
    "unicorn/prefer-at":                            ["error"],
    "unicorn/prefer-logical-operator-over-ternary": ["error"],
    "unicorn/prefer-negative-index":                ["error"],
    "unicorn/prefer-switch":                        ["error"],
    "vue/array-bracket-newline":                    ["error", { minItems: 5, multiline: true }],
    "vue/attributes-order":                         ["error"],
    "vue/define-emits-declaration":                 ["error"],
    "vue/define-props-declaration":                 ["error"],
    "vue/no-empty-component-block":                 ["error"],
    "vue/no-multiple-template-root":                ["error"],
    "vue/require-typed-ref":                        ["error"],
  },
})
