## Sample 003

**Source**: `ai-sdk-fix\skills\add-provider-package\SKILL.md` L36

```
packages/<provider>/
├── src/
│   ├── index.ts                  # Main exports
│   ├── version.ts                # Package version
│   ├── <provider>-provider.ts    # Provider implementation
│   ├── <provider>-provider.test.ts
│   ├── <provider>-*-options.ts   # Model-specific options
│   └── <provider>-*-model.ts     # Model implementations (e.g., language, embedding, image)
├── package.json
├── tsconfig.json
├── tsconfig.build.json
├── tsup.config.ts
├── turbo.json
├── vitest.node.config.js
├── vitest.edge.config.js
└── README.md
```

