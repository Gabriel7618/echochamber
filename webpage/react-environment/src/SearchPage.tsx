import { useState } from 'react'
import { Input, Spin, Button} from "antd"
import { useNavigate } from "react-router-dom"
import { ThreeColumnLayout } from "./components/ThreeColumnLayout";
import { columnStyle, borderedStyle } from "./components/styles/columnStyles";
import { PaginatedButtonColumn } from './components/PaginatedButtonColumn';

/* Search component */
function SearchPage() {
  // we are defining two pieces of state: loading = whether to show the loading screen or not
  // and query = the term being searched which we'll need for the API use
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const navigate = useNavigate(); // allows us to go back to homepage

  const mockArticleList = [
    { title: "First", excerpt: "first excerpt", url: "https://www.wikipedia.org/"},
    { title: "Second", excerpt: "second excerpt", url: "https://www.wikipedia.org/"},
    { title: "Third", excerpt: "third excerpt", url: "https://www.wikipedia.org/"},
    { title: "Fourth", excerpt: "fourth excerpt", url: "https://www.wikipedia.org/"},
    { title: "Fifth", excerpt: "fifth excerpt", url: "https://www.wikipedia.org/"}
  ];

  // we are defining a function to set the loading screen once a search query has been entered
  const handleSearch = (value: string) => {
    setQuery(value);
    setLoading(true); // these variables have now been updated
    setShowResults(false);

    // now we can simulate the loading state (will need to replace this with API cal  l later)
    setTimeout(() => {
      console.log("Search complete for:", value);
      setLoading(false);
      setShowResults(true); 
    }, 2000); // fake loading rn 
  };

  return (
    // page fades in when it loads — using the CSSTransition wrapper
    // When displaying articles change the container such that it fills more of the screen
      <div className={`${!loading && showResults ? "article-container fade-in" : "search-container"} fade-in`}>
        {// adding a back button to homepage //
        }
        <Button onClick={() => navigate("/")}>
          ← Back to Homepage
        </Button>

        <h1>EchoChamber Search</h1>

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
                    <p><PaginatedButtonColumn articles={mockArticleList} /></p>
                  </div>}
          center = {<div style={{ ...columnStyle, ...borderedStyle }}>
                      <p><PaginatedButtonColumn articles={mockArticleList} /></p>
                    </div>}
          right = {<div style={columnStyle}>
                     <p><PaginatedButtonColumn articles={mockArticleList} /></p>
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
