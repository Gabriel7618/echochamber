import { Breadcrumb } from "antd";
import { Link, useLocation } from "react-router-dom";

const breadcrumbNameMap: Record<string, string> = {
  "/": "Home",
  "/search": "Search Page",
};

export const BreadcrumbNav = () => {
  const location = useLocation();
  const pathSnippets = location.pathname.split("/").filter(i => i);

  const extraBreadcrumbItems = pathSnippets.map((_, index) => {
    const url = `/${pathSnippets.slice(0, index + 1).join("/")}`;
    return {
      key: url,
      title: <Link to={url}>{breadcrumbNameMap[url] || url}</Link>,
    };
  });

  const breadcrumbItems = [
    {
      key: "home",
      title: <Link to="/">Home</Link>,
    },
    ...extraBreadcrumbItems,
  ];

  return <Breadcrumb items={breadcrumbItems} />;
};
