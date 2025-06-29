import React, { useState, useEffect } from 'react';
import './ThemeToggler.css';

const ThemeToggler = () => {
  const [theme, setTheme] = useState('dark');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prevTheme => (prevTheme === 'dark' ? 'light' : 'dark'));
  };

  return (
    <button onClick={toggleTheme} className="theme-toggler" aria-label="Toggle theme">
      <span className="sun">☀️</span>
      <span className="moon">🌙</span>
    </button>
  );
};

export default ThemeToggler;