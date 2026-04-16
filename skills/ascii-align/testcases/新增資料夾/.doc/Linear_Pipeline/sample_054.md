## Sample 054

**Source**: `Claude-Code-Agent-Monitor\client\README.md` L147

```
client/
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── __tests__/      # Component tests
│   │   ├── AgentCard.tsx
│   │   ├── SessionCard.tsx
│   │   ├── ToolCard.tsx
│   │   ├── EventTimeline.tsx
│   │   ├── NotificationBadge.tsx
│   │   └── Layout.tsx
│   │
│   ├── pages/              # Route pages
│   │   ├── SessionsPage.tsx
│   │   ├── SessionDetailPage.tsx
│   │   ├── AgentDetailPage.tsx
│   │   ├── SettingsPage.tsx
│   │   └── PricingPage.tsx
│   │
│   ├── lib/                # Core utilities & business logic
│   │   ├── __tests__/      # Utility tests
│   │   ├── api.ts          # REST API client
│   │   ├── websocket.ts    # WebSocket manager
│   │   ├── eventBus.ts     # Event pub/sub
│   │   ├── notifications.ts # Browser notifications
│   │   ├── format.ts       # Formatters (fmt, fmtCost, timeAgo)
│   │   ├── types.ts        # TypeScript type definitions
│   │   └── constants.ts    # App-wide constants
│   │
│   ├── App.tsx             # Root component
│   ├── main.tsx            # Entry point
│   └── index.css           # Global styles (Tailwind imports)
│
├── public/                 # Static assets
├── index.html              # HTML template
├── vite.config.ts          # Vite configuration
├── vitest.config.ts        # Test configuration
├── tailwind.config.js      # Tailwind CSS config
├── tsconfig.json           # TypeScript config
└── package.json
```

