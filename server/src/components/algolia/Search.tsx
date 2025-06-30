'use client';

import React from "react";
import { Configure, Hits, InstantSearch } from "react-instantsearch";
import Autocomplete from "@/lib/agolia/AutoComplete";
import HitComponent from "@/lib/agolia/hit";
import { searchClient } from "@/lib/agolia/searchClient";
import { INSTANT_SEARCH_INDEX_NAME } from "@/lib/constant";
import "./Search.css"; // Import the new stylesheet
import ThemeToggler from "./ThemeToggler";
import { history } from 'instantsearch.js/es/lib/routers';
import TerminalSearch from "./TerminalSearch";

export default function Search() {
  return (
    <InstantSearch
      searchClient={searchClient}
      indexName={INSTANT_SEARCH_INDEX_NAME}
      future={{
        preserveSharedStateOnUnmount: true,
      }}
      routing={{
        router: history({
            cleanUrlOnDispose: false,
        }),

      }}
    >
      <Configure hitsPerPage={200} distinct={true} getRankingInfo={true}/>
      <div className="search-container">
        <ThemeToggler />
        <h1 className="cyber-search-title">Personal Blogs and Articles</h1>
        <TerminalSearch>
          <Autocomplete
            searchClient={searchClient}
            placeholder=""
            detachedMediaQuery="none"
            className="cyber-search"
            openOnFocus
          />
        </TerminalSearch>
        <div className="hits-grid">
          <Hits hitComponent={({ hit }) => <HitComponent hit={hit} />} />
        </div>
      </div>
    </InstantSearch>
  );
}