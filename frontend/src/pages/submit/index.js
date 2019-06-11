import React, { Component } from 'react';
import router from 'umi/router';
import { Button, List, Rate } from 'antd';
import axios from 'axios';
import styles from './index.scss';

const AnalysisAPI = "/api/analysis/";

class Submit extends Component {
    constructor(props) {
        super(props);
        this.state = {
            jobList: [],
        };
    }

    handleAnalysis = () => {
        const { duty, require } = this.props.location.state;
        const user_chosen = {};
        user_chosen.like = duty;
        user_chosen.cando = require;
        axios.post(AnalysisAPI, {
            user_chosen_dict: user_chosen,
        }).then((response) => {
            const respData = response.data;
            this.setState({ jobList: respData });
        }).catch((err) => {
            console.log(err);
        })
    }

    componentDidMount = () => {
        if (this.props.location.state === undefined) {
            router.push('/');
        } else {
            this.handleAnalysis();
        }
    }

    reTest = () => {
        router.push('/');
    }

    render() {
        return (
            <div>
                <h3 className={styles.discrib}>适合你的职位可能是：</h3>
                <p><List
                    bordered
                    dataSource={this.state.jobList}
                    renderItem={item => <List.Item>{item[0]} <Rate disabled defaultValue={Math.round(item[1]/20)} /></List.Item>}
                /></p>
                <p className={styles.button}><Button type="primary" onClick={this.reTest}>再试一次</Button></p>
            </div>
        );
    }
}
export default Submit;

