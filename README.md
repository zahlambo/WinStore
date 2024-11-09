# WinStore

This project allows you to select and install all apps that you need for your windows machine. This is especially helpful when you install fresh windows frequently.

# Backend
Zahir should write how to get started and contribute in BE in here.

# Frontend
```
/frontend
├── /public
│   ├── /assets                # Static files like images, fonts, etc.
│   │   ├── logo.png
│   │   ├── group              # Group a specific type of asset
│   │   └── ...
├── /src
│   ├── /components            # Reusable UI components
│   │   ├── Header.js
│   │   ├── Button.js
│   │   └── ...
│   ├── /containers            # Larger, more complex components, typically with state
│   │   ├── Dashboard.js
│   │   ├── UserProfile.js
│   │   └── ...
│   ├── /pages                 # Page components (routes)
│   │   ├── HomePage.js
│   │   ├── AboutPage.js
│   │   └── ...
│   ├── /hooks                 # Custom React hooks
│   │   ├── useAuth.js
│   │   └── ...
│   ├── /services              # API calls and external services
│   │   ├── api.js
│   │   └── ...
│   ├── /context               # React Context API or Redux-related files
│   │   ├── AuthContext.js
│   │   └── ...
│   ├── /utils                 # Utility functions
│   │   ├── formatDate.js
│   │   └── ...
│   ├── /styles                # Global styles, theme settings
│   │   ├── index.css
│   │   └── theme.js
│   ├── main.tsx                 # Main App component
│   ├── index.html               # Entry point to the app, where ReactDOM renders the App
│   └── /routes.js             # All the routing logic (optional, if needed)
├── /node_modules
├── package.json
├── README.md
├── .eslint.config.js               # Different Configuration files
└── ...

```