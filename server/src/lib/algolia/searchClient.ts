import { liteClient as algoliasearch } from 'algoliasearch/lite';
import dotenv from 'dotenv';
dotenv.config();
const appId = process.env.NEXT_PUBLIC_ALGOLIA_APP_ID || 'your-app-id'; ;
const apiKey = process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_API_KEY || 'your-search-api-key';

if (!appId || !apiKey) {
  throw new Error('Algolia app ID and API key must be set in environment variables');
}

export const searchClient = algoliasearch(appId, apiKey);