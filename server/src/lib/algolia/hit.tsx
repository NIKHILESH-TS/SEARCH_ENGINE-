import React, { useRef, useEffect } from "react";
import './hit.css'; // Import the new stylesheet
import type { BaseHit } from 'instantsearch.js';

type HitProps = {
  hit: BaseHit & {
    title?: string;
    description?: string;
    url?: string;
    [key: string]: unknown;
  };
};

function getFavicon(url?: string) {
  if (!url) return null;
  try {
    const { hostname } = new URL(url);
    return `https://www.google.com/s2/favicons?domain=${hostname}`;
  } catch {
    return null;
  }
}

const HitComponent: React.FC<HitProps> = ({ hit }) => {
  const favicon = getFavicon(hit.url);
  const cardRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const card = cardRef.current;
    if (!card) return;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      card.style.setProperty('--mouse-x', `${(x / rect.width) * 100}%`);
      card.style.setProperty('--mouse-y', `${(y / rect.height) * 100}%`);
    };

    card.addEventListener('mousemove', handleMouseMove);

    return () => {
      card.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  const handleClick = () => {
    if (hit.url) {
      window.open(hit.url, '_blank', 'noopener,noreferrer');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (hit.url && (e.key === 'Enter' || e.key === ' ')) {
      e.preventDefault();
      handleClick();
    }
  };

  return (
    <div className="holographic-card-wrapper w-full flex justify-center">
      <div
        ref={cardRef}
        className={`holographic-card w-[70vw] max-w-3xl min-w-[300px] ${hit.url ? 'cursor-pointer' : ''}`}
        onClick={hit.url ? handleClick : undefined}
        onKeyDown={handleKeyDown}
        role={hit.url ? 'link' : undefined}
        tabIndex={hit.url ? 0 : undefined}
      >
        <div className="holographic-card-glow"></div>
        <article className="holographic-card-content">
          <header className="flex items-center gap-3">
            {favicon && (
              <img
                src={favicon}
                alt="Favicon"
                className="w-6 h-6 rounded-full shadow-lg border-2 border-white/50"
                aria-hidden="true"
                loading="lazy"
              />
            )}
            <h2 className="text-xl font-bold break-words text-white drop-shadow-[0_2px_5px_rgba(0,246,255,0.7)]">
              {hit.title || <span className="italic text-gray-300">No title</span>}
            </h2>
          </header>
          <p className="text-gray-200">
            {hit.description || <span className="italic text-gray-400">No description available.</span>}
          </p>
        </article>
      </div>
    </div>
  );
};

export default HitComponent;