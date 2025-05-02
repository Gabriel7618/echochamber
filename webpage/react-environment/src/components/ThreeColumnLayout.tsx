import { Row, Col } from "antd";
import React from "react";

type ThreeColumnLayoutProps = {
  left: React.ReactNode;
  center: React.ReactNode;
  right: React.ReactNode;
};

/* Creates three equally sized columns and allows arguments for what goes into each column */
export const ThreeColumnLayout = ({ left, center, right }: ThreeColumnLayoutProps) => {
  return (
    <Row>
      <Col span={8} style={{ height: "100%" }}>{left}</Col>
      <Col span={8} style={{ height: "100%" }}>{center}</Col>
      <Col span={8} style={{ height: "100%" }}>{right}</Col>
    </Row>
  );
};
