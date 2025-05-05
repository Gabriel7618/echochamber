import { Button } from "antd";

type LinkButtonProps = {
  title: string;
  url: string;
};


/* custom button which has underlined text, a reduced border and custom font size
   used for the article titles, when clicked open the accossiated url in a new tab */
export const LinkButton = ({ title, url }: LinkButtonProps) => {
  return (
    <Button
      type="text"
      className="link-button"
      href={url}
      target="_blank"
      rel="noopener noreferrer"
    >
      {title}
    </Button>
  );
};
