import React, { Component } from 'react';
import { Button } from 'antd';
import router from 'umi/router';
import styles from './index.scss';


class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  handleClick = () => {
    router.push('/select');
  }
  
  render() {
    return (
      <div>
        <p className={styles.welcome} />
        <p className={styles.button}><Button type='primary' size='large' onClick={this.handleClick}>开始测试</Button></p>
      </div>
    );
  }
}
export default Home;

