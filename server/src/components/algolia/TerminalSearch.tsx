import React, { useState, useEffect, ReactElement } from 'react';
import './TerminalSearch.css';

interface TerminalSearchProps {
  children: ReactElement;
}

const TerminalSearch: React.FC<TerminalSearchProps> = ({ children }) => {
  const [placeholder, setPlaceholder] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const fullPlaceholder = 'Initiate search sequence...';

  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      setPlaceholder(fullPlaceholder.substring(0, i + 1));
      i++;
      if (i > fullPlaceholder.length) {
        clearInterval(interval);
      }
    }, 100);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="terminal-search-wrapper">
      <div className="terminal-search">
        <span className="prompt">&gt;</span>
        <div
          style={{ position: 'relative', flex: 1 }}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
        >
          {children}
          {!isFocused && (
            <span
              className="terminal-placeholder"
              style={{
                position: 'absolute',
                left: 0,
                top: 0,
                color: 'rgba(0,246,255,0.5)',
                pointerEvents: 'none',
                fontFamily: 'inherit',
                fontSize: '1.2rem',
                paddingLeft: '0.25rem',
                paddingTop: '0.1rem',
                zIndex: 2,
              }}
            >
              {placeholder}
            </span>
          )}
        </div>
        <span className="cursor"></span>
      </div>
    </div>
  );
};

export default TerminalSearch;
