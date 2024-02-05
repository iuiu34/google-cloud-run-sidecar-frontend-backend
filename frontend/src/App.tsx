import React, {useState} from 'react';
import {Breadcrumb, Button, Layout, Menu, theme} from 'antd';

const {Header, Content, Footer} = Layout;

const items = new Array(15).fill(null).map((_, index) => ({
    key: index + 1,
    label: `nav ${index + 1}`,
}));

declare global {
    interface Window {
        env: {
            BACKEND_URL?: string;
        };
    }
}

const fetchBackend = async (endpoint: string) => {
    try {
        const backendUrl = window.env?.BACKEND_URL || 'http://127.0.0.1:8000';
        console.log(backendUrl, 'backendUrl')
        const url = `${backendUrl}/${endpoint}`;
        console.log(url, 'url')
        const response = await fetch(url,
            {
                headers: {
                    'Frontend-Call': 'true'
                }
            });
        console.log(response, 'response')
        const data = await response.json();
        console.log(data, 'data')
        return data;
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
};

const App: React.FC = () => {
    const {
        token: {colorBgContainer, borderRadiusLG},
    } = theme.useToken();

    const [showText, setShowText] = useState(false);
    const [n, setAdd] = useState(0);
    const [randomNumber, setRandomNumber] = useState<number | null>(null);
    // const backendUrl = process.env.REACT_APP_BACKENDURL || 'http://127.0.0.1:8000';
    // const backendUrl = 'http://127.0.0.1:8000';
    // cache
    const fetchRandomNumber = async () => {
        const data = await fetchBackend("get_random_number")
        setRandomNumber(data?.random_number);
    };

    const handleClick = () => {
        setAdd(n + 1);
        setShowText(!showText);
        if (!showText) {
            fetchRandomNumber();
        }

    };

    const content = (
        <div>
            <p> Hello World</p>
            <p> n is {n}</p>
            <Button type="primary" onClick={handleClick}>Click me</Button>
            {showText && <p> random number {randomNumber}</p>}
        </div>
    );

    return (
        <Layout>
            <Header style={{display: 'flex', alignItems: 'center'}}>
                <div className="demo-logo"/>
                <Menu
                    theme="dark"
                    mode="horizontal"
                    defaultSelectedKeys={['2']}
                    items={items}
                    style={{flex: 1, minWidth: 0}}
                />
            </Header>
            <Content style={{padding: '0 48px'}}>
                <Breadcrumb style={{margin: '16px 0'}}>
                    <Breadcrumb.Item>Home</Breadcrumb.Item>
                    <Breadcrumb.Item>List</Breadcrumb.Item>
                    <Breadcrumb.Item>App</Breadcrumb.Item>
                </Breadcrumb>
                <div
                    style={{
                        background: colorBgContainer,
                        minHeight: 280,
                        padding: 24,
                        borderRadius: borderRadiusLG,
                    }}
                >
                    {content}
                </div>
            </Content>
        </Layout>
    );
};

export default App;