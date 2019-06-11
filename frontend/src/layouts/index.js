import { Component } from 'react';
import { Layout } from 'antd';
import styles from './index.scss';

const { Header, Footer, Content } = Layout;

class BasicLayout extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    return (
      <Layout className={styles.normal}>
        <Layout >
          <Header className={styles.header}>SuitJOB</Header>
          <Content className={styles.content}>
            <div className={styles.children}>
              {this.props.children}
            </div>
          </Content>
          <Footer className={styles.footer}>©2019 Created by Yam</Footer>
        </Layout>
      </Layout>
      )
    }
  }
  
export default BasicLayout;