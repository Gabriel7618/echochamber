import './App.css'
import './transitions.css' // fade-in/out animation stuff

import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import HomePage from './HomePage'
import SearchPage from './SearchPage'

// This is to set up the different paths
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/search" element={<SearchPage />} />
      </Routes>
    </Router>
  );
}

export default App;


/* This was my initial test for a dummy search bar -- i build on this
      <Input.Search
        placeholder="Enter a topic..."
        enterButton="Search"
        size="large"
        onSearch={(value) => console.log("Search query:", value)}
      />
*/


// extra things i needed to do in terminal:
// had to install antd, node.js and react-router-dom to get the icons and different pages /homepage and /search