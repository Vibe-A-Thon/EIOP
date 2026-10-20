/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly REACT_APP_BACKEND_URL: string;
  readonly VITE_API_BASE?: string;
  // Development-only quick-login tokens (untracked frontend/.env.local; never committed).
  readonly VITE_DEV_TOKEN?: string;
  readonly VITE_DEMO_TOKEN_SUPERADMIN?: string;
  readonly VITE_DEMO_TOKEN_ADMIN?: string;
  readonly VITE_DEMO_TOKEN_STEWARD?: string;
  readonly VITE_DEMO_TOKEN_ANALYST?: string;
  readonly VITE_DEMO_TOKEN_VIEWER?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
