// src/pages/HomePage.tsx
import React from 'react';
import { Typography } from 'antd';

const { Title } = Typography;

const HomePage: React.FC = () => {
  return (
    <div>
      <Title level={2}>Home Page</Title>
      <p>This is the home page.</p>
    </div>
  );
};

export default HomePage;