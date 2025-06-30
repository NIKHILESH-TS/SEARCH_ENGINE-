<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<div align="center">
    <a href="https://github.com/NIKHILESH-TS/SEARCH_ENGINE-">
        <img src="https://readme-typing-svg.herokuapp.com/?lines=Search%20Engine&font=Fira%20Code&center=true&width=380&height=50&duration=4000&pause=1000" alt="Project Logo">
    </a>
    <p>
        A simple search engine built with Next.js and Algolia.<br><br>
        Try searching for something like "web development" or "machine learning" to see how it works!
    </p>
    <h2><a href="https://search-engine-lovat-nine.vercel.app/">Click here to visit our site</a></h2>
</div>

<!-- TABLE OF CONTENTS -->
<details>
    <summary>Table of Contents</summary>
    <ol>
        <li>
            <a href="#about-the-project">About The Project</a>
            <ul>
                <li><a href="#built-with">Built With</a></li>
            </ul>
        </li>
        <li>
            <a href="#getting-started">Getting Started</a>
            <ul>
                <li><a href="#prerequisites">Prerequisites</a></li>
            </ul>
        </li>
        <li><a href="#usage">Usage</a></li>
        <li><a href="#features">Features</a></li>
        <li><a href="#web-crawler">Web Crawler</a></li>
        <li><a href="#algolia-search">Algolia Search</a></li>
        <li><a href="#license">License</a></li>
        <li><a href="#contact">Contact</a></li>
    </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

This project is a simple but powerful search engine built with Next.js and Algolia. We created it to make finding information quick and easy - just type what you're looking for and get results instantly!.

Key highlights:

- **Super fast results** - Algolia's search algorithm returns matches in milliseconds
- **User-friendly interface** - Clean design that works on both desktop and mobile
- **Easy to customize** - Add your own data and style it however you want

We built this as part of our exploration of modern web technologies and to create something actually useful that others can build upon.
We're cutting through the noise of generic, SEO-driven search results. This project prioritizes and indexes high-quality content from personal blogs and experienced professionals—the kind of valuable insight that usually gets lost. Our goal is to provide a search experience that delivers meaningful articles and advice, free from corporate clutter.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![Next][Next.js]][Next-url]
- [![React][React.js]][React-url]
- [![Algolia][Algolia.com]][Algolia-url]
- [![python][Python]][Python-url]
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

Getting this search engine up and running is super simple! Just follow these steps:

### Project Structure

```
serach-engine/
├── scripts/           # Python crawler scripts
│   ├── final_bot.py   # Main crawler script
|── server/             # Next.js server files
    ├── src/
    │   ├── app/               # Next.js App Router
    │   ├── components/
    │   │   └── agolia/        # Algolia-specific components
    │   │       ├── Search.tsx # Main search container
    │   │       ├── TerminalSearch.tsx
    │   │       └── ThemeToggler.tsx
    │   ├── lib/
    │   │   ├── constant.ts    # Project constants
    │   │   └── agolia/        # Algolia configuration
    │   │       ├── AutoComplete.tsx
    │   │       ├── hit.tsx    # Result card component
    │   │       └── searchClient.ts

```

### Prerequisites

- Node.js and npm installed on your computer
- An Algolia account (free tier works fine!)

### Step 1: Get the code

Clone the repository to your computer:

```sh
git clone https://github.com/NIKHILESH-TS/SEARCH_ENGINE-.git
cd SEARCH_ENGINE-/server/
```

### Step 2: Install dependencies

```sh
npm install
```

### Step 3: Set up your environment

Create a file called `.env.local` in the main folder and add your Algolia details:

```
NEXT_PUBLIC_ALGOLIA_APP_ID=your_app_id_from_algolia
NEXT_PUBLIC_ALGOLIA_SEARCH_API_KEY=your_search_key_from_algolia
NEXT_PUBLIC_ALGOLIA_INDEX_NAME=your_index_name
```

### Step 4: Start the app

```sh
npm run dev
```

That's it! Your search engine should now be running at http://localhost:3000 🎉

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Features

🔍 **Powerful Search** - Find exactly what you need with Algolia's advanced search capabilities

- Typo-tolerant search (still finds results even with spelling mistakes)
- Highlighting of matching terms in search results
- Filtering and faceting options

🚀 **Fast Performance** - Built with Next.js for optimal speed and user experience

- Server-side rendering for fast initial page loads
- Client-side navigation for smooth transitions between pages
- Optimized for both desktop and mobile devices

🕸️ **Custom Web Crawler** - Our Python crawler collects data from websites to power the search

- Respects robots.txt rules
- Extracts relevant content from web pages
- Formats data for Algolia indexing

✨ **Modern UI** - Clean, intuitive interface that makes searching a pleasure

- Responsive design works on all screen sizes
- Instant feedback as you type
- Customizable result display

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Web Crawler

We created our own web crawler using Python to collect data for our search engine. It's simple but does the job well!

### How our crawler works:

1. **Checks the rules first** - Looks at robots.txt to make sure we're allowed to crawl the site
2. **Grabs the content** - Downloads the HTML from web pages
3. **Finds the good stuff** - Uses BeautifulSoup to extract titles, descriptions, links, etc.
4. **Gets it ready for search** - Formats everything into JSON that Algolia can use

### Want to use the crawler?

The crawler code is in the `scripts` folder. To run it:

```sh
cd scripts
python final_bot.py
```

Urls need to be passed as a list in the `urls` variable inside `final_bot.py`. For example:

```python
urls = [
    "https://example.com",
    "https://another-example.com"
]
```

The results will be saved to `output.json` which you can then upload to Algolia.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Algolia Search

### What is Algolia?

Algolia is a search-as-a-service platform that makes it easy to add powerful search functionality to your website or app. It's what makes our search engine so fast and accurate!

### Setting up Algolia (it's easy!)

1. **Sign up** - Create a free account at [Algolia](https://www.algolia.com/)
2. **Create an index** - This is where your search data will live
3. **Get your API keys** - You'll need these to connect your app to Algolia
4. **Add them to your project** - Put your keys in the `.env` file:
   ```
   NEXT_PUBLIC_ALGOLIA_APP_ID=your_app_id
   NEXT_PUBLIC_ALGOLIA_SEARCH_API_KEY=your_search_api_key
   NEXT_PUBLIC_ALGOLIA_INDEX_NAME=your_index_name
   ```

### Adding data to Algolia

You can add data in several ways:

- Upload a JSON file through the Algolia dashboard
- Use our web crawler to collect and format data
- Add data manually through the Algolia API

### The free tier is generous!

- 10,000 search requests per month
- Up to 10,000 records
- Perfect for small to medium projects

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Key Features

- Instant search results with Algolia
- Responsive design with Next.js
- Easy to set up and customize

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## License

Distributed under the MIT License . See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

- Lalith Sai - Discord: `@lalith_sai_x7777`
- Nikhilesh - Discord: `@nikhilesh_ts`

Project Link: [https://github.com/NIKHILESH-TS/SEARCH_ENGINE-](https://github.com/NIKHILESH-TS/SEARCH_ENGINE-)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Algolia.com]: https://img.shields.io/badge/Algolia-5468FF?style=for-the-badge&logo=algolia&logoColor=white
[Algolia-url]: https://www.algolia.com/
[Python-url]: https://www.python.org/
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[product-screenshot]: images/screenshot.png
[search-screenshot]: images/search-example.png

<!-- USAGE -->

## Usage

Using the search engine is as intuitive as it gets:

### Basic Usage

1. Type your search query in the search bar
2. Results appear instantly as you type
3. Click on a result to go to that page

Try searching for something like "web development" or "machine learning" to see how it works!

### Adding Your Own Data

To add your own websites or content to the search:

1. Use our web crawler on your site
2. Upload the generated JSON to Algolia
3. Update your `.env` file with the new index name

Need more help? Check out the [Algolia documentation](https://www.algolia.com/doc/) for advanced features.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Algolia.com]: https://img.shields.io/badge/Algolia-5468FF?style=for-the-badge&logo=algolia&logoColor=white
[Algolia-url]: https://www.algolia.com/
[Python-url]: https://www.python.org/
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
