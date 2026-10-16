import React, {createContext, useContext, useEffect, useState} from 'react';

const STORAGE_KEY = 'eoip-graph-theme';
const ThemeContext = createContext({theme: 'light', setTheme: () => {}});

export function useTheme() {
  return useContext(ThemeContext);
}

export function ThemeProvider({children, defaultTheme = 'light', storageKey = STORAGE_KEY}) {
  const [theme, setTheme] = useState(() => {
    try {
      return sessionStorage.getItem(storageKey) || defaultTheme;
    } catch {
      return defaultTheme;
    }
  });

  useEffect(() => {
    try {
      sessionStorage.setItem(storageKey, theme);
    } catch {
      /* storage unavailable */
    }
  }, [theme, storageKey]);

  return (
    <ThemeContext.Provider value={{theme, setTheme}}>
      <div className={`eoip-graph-theme eoip-theme-${theme}`} data-theme={theme}>
        {children}
      </div>
    </ThemeContext.Provider>
  );
}

export function ThemeToggle({labels = {light: 'Light', dark: 'Dark'}}) {
  const {theme, setTheme} = useTheme();
  const next = theme === 'dark' ? 'light' : 'dark';
  return (
    <button
      type="button"
      className="enh-button"
      aria-label={`Switch to ${next} theme`}
      aria-pressed={theme === 'dark'}
      onClick={() => setTheme(next)}
    >
      <span aria-hidden="true">{theme === 'dark' ? '☀' : '☾'}</span> {labels[theme] || theme}
    </button>
  );
}
