import { useState } from 'react'
import { Input, Spin, Button } from "antd"
import { useNavigate } from "react-router-dom"

/* Search component */
function SearchPage() {
  // we are defining two pieces of state: loading = whether to show the loading screen or not
  // and query = the term being searched which we'll need for the API use
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const navigate = useNavigate(); // allows us to go back to homepage

  const mockResults = {
    positive: [{ title: "Positive News", excerpt: "Supportive text...", url: "#" }],
    neutral: [{ title: "Neutral News", excerpt: "Neutral reporting...", url: "#" }],
    negative: [{ title: "Negative News", excerpt: "Critical text...", url: "#" }],
  };

  // we are defining a function to set the loading screen once a search query has been entered
  const handleSearch = (value: string) => {
    setQuery(value);
    setLoading(true); // these variables have now been updated
    setShowResults(false);

    // now we can simulate the loading state (will need to replace this with API call later)
    setTimeout(() => {
      console.log("Search complete for:", value);
      setLoading(false);
      setShowResults(true); 
    }, 2000); // fake loading rn 
  };

  return (
    // page fades in when it loads — using the CSSTransition wrapper
      <div className="container fade-in">
        {// adding a back button to homepage //
        }
        <Button style={{ marginBottom: "1.5rem" }} onClick={() => navigate("/")}>
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
          <div>
            {/* show the 3 col results here */}
          </div>
        )}
      </div>
  );
}

export default SearchPage;
