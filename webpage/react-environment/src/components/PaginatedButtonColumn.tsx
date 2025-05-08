import { useState } from 'react'
import { Pagination } from "antd";
import { LinkButton } from "./LinkButton"; 

type Article = {
  title: string;
  excerpt: string;
  url: string;
};

type Props = {
  articles: Article[];
};


/* This splits up a given list of articles into batches of 4 and then presents each set on a different page
selected using ant designs pagination component */
export const PaginatedButtonColumn = ({ articles }: Props) => {
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 4;
  const startIndex = (currentPage - 1) * pageSize; 
  const endIndex = startIndex + pageSize;
  const currentItems = articles.slice(startIndex, endIndex);

  return (
    <div style={{ textAlign: "left" }}>
      {currentItems.map((item, index) => (
        <div key={index} style={{ marginBottom: "0.5rem" }}>
          <LinkButton title={item.title} url={item.url} />
          <div style={{ fontSize: "12px" }}>
            {item.excerpt}
            </div>
        </div>
      ))}

      <Pagination
        current={currentPage}
        pageSize={pageSize}
        total={articles.length}
        onChange={setCurrentPage}
        showSizeChanger={false}
        size="small"
        style={{ marginTop: "1rem", textAlign: "center" }}
      />
    </div>
  );
};
