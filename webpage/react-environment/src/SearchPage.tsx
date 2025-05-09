import { useState } from 'react'
import { Input, Spin } from "antd"
import { ThreeColumnLayout } from "./components/ThreeColumnLayout";
import { columnStyle, borderedStyle } from "./components/styles/columnStyles";
import { PaginatedButtonColumn } from './components/PaginatedButtonColumn';
import { BreadcrumbNav

 } from './components/breadcrumbNavigation';
/* Define some data types for our articles and the responce from our API call */
type Article = {
  title: string;
  excerpt: string;
  url: string;
};

type ArticleResponse = {
  supportive: Article[];
  opposing: Article[];
  neutral: Article[];
};

/* Search component */
function SearchPage() {
  // we are defining two pieces of state: loading = whether to show the loading screen or not
  // and query = the term being searched which we'll need for the API use
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const [supportiveArticles, setSupportiveArticles] = useState<Article[]>([]);
  const [neutralArticles, setNeutralArticles] = useState<Article[]>([]);
  const [opposingArticles, setOpposingArticles] = useState<Article[]>([]);

  function decodeHtml(html: string) {
    const txt = document.createElement("textarea");
    txt.innerHTML = html;
    return txt.value;
  }
  
  function cleanArticles(articles: Article[]) {
    return articles.map(article => ({
      title: article.title,
      excerpt: decodeHtml(article.excerpt.replace(/<[^>]*>/g, "")), // remove HTML tags + decode
      url: article.url
    }));
  }

  // we are defining a function to set the loading screen once a search query has been entered
	const handleSearch = async (value: string) => {
		setQuery(value);
		setLoading(true);
		setShowResults(false);

		try {
			const response = await fetch(`http://127.0.0.1:8000/articles/${encodeURIComponent(value)}`);
			const data: ArticleResponse = await response.json();

      setSupportiveArticles(cleanArticles(data.supportive));
      setNeutralArticles(cleanArticles(data.neutral));
      setOpposingArticles(cleanArticles(data.opposing));

      console.log("Positive Article list:")
      console.log(data.supportive)
      console.log("Neutral Article list:")
      console.log(data.neutral)
      console.log("Negative Article list:")
      console.log(data.opposing)

		} catch (error) {
			console.error("Error fetching articles:", error);
			setSupportiveArticles([]);
      setNeutralArticles([])
      setOpposingArticles([])
		}

		setLoading(false);
		setShowResults(true);
	};

  return (
    // page fades in when it loads — using the CSSTransition wrapper
    // When displaying articles change the container such that it fills more of the screen
      <div className={`${!loading && showResults ? "article-container fade-in" : "search-container"} fade-in`}>
        {// Add a breadcrumb to allow users to return back to the hompage //
        }
        <BreadcrumbNav />
        <h1 style={{marginTop: "0.2rem"}}>EchoChamber Search</h1>

        {// if loading show the spinner (aka after user clicks search button)
        }
        {loading && (
          <div style={{ textAlign: "center", marginTop: "3rem" }}>
            <Spin size="large" tip="Loading articles..." />
          </div>
        )}

        {// if not loading and results not ready, show the search bar
        }
        {!loading && !showResults && (
          <Input.Search
            placeholder="Enter a topic..."
            enterButton="Search"
            size="large"
            onSearch={handleSearch}
          />
        )}

        {// if not loading and results ready, show the articles
        }
        {!loading && showResults && (
          // Keep the search bar so we can search for something new, make the placeholder text the current query
          <div className="slower-fade-in">
          <Input.Search
          placeholder={query}
          enterButton="Search"
          size="large"
          onSearch={handleSearch}
          // Positive, Neutral and Negative titles above the three columns
          />
          <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
          <ThreeColumnLayout
          left = {<div style={columnStyle}>
                    <p style={{ marginBottom: "0rem" }}> <span className="positive"> <strong> Positive</strong></span></p>
                  </div>}
          center = {<div style={columnStyle}>
                      <p style={{ marginBottom: "0rem" }}> <span className="neutral"> <strong> Neutral</strong></span></p>
                    </div>}
          right = {<div style={columnStyle}>
                     <p style={{ marginBottom: "0rem" }}> <span className="negative"> <strong> Negative</strong></span></p>
                   </div>}
          />
          <div style={{ flexGrow: 1 }}>
          <ThreeColumnLayout
          left = {<div style={columnStyle}>
                    <p><PaginatedButtonColumn articles={supportiveArticles} /></p>
                  </div>}
          center = {<div style={{ ...columnStyle, ...borderedStyle }}>
                      <p><PaginatedButtonColumn articles={neutralArticles} /></p>
                    </div>}
          right = {<div style={columnStyle}>
                     <p><PaginatedButtonColumn articles={opposingArticles} /></p>
                   </div>}
          />
          </div>
          </div>
          </div>
        )}
      </div>
  );
}

export default SearchPage;
