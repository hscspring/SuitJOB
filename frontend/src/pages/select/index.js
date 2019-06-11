import React, { Component } from 'react';
import axios from 'axios';
import router from 'umi/router';
import { Button, Checkbox, message } from 'antd';
import styles from './index.scss';

const InitAPI = "/api/init/";

const Dsiplay = (props) => {
    if (props.state.isNext) {
        return (
            <div>
                <h3 className={styles.discrib}>请选择你喜欢的描述（尽可能多选）：</h3>
                <p><Checkbox.Group className={styles['ant-checkbox-wrapper']} options={props.state.likeOptions} defaultValue={[]} onChange={props.onDutyChange} /></p>
                <p className={styles.button}><Button type='primary' onClick={props.onNext}>下一步</Button></p>
            </div>
        )
    } else {
        return (
            <div>
                <h3 className={styles.discrib}>请选择你已经或可能具备的（尽可能多选）：</h3>
                <p><Checkbox.Group className={styles['ant-checkbox-wrapper']} options={props.state.candoOptions} defaultValue={[]} onChange={props.onRequireChange} /></p>
                <p className={styles.button}><Button type='primary' onClick={props.onSubmit}>提交</Button></p>
            </div>
        )
    }
}
        
class UserSelect extends Component {
    constructor(props) {
        super(props);
        this.state = {
            likeOptions: [],
            candoOptions: [],
            duty: [],
            require: [],
            isNext: true,
        };
    }

    handleOptions = (itemList) => {
        let res = [];
        itemList.forEach(ele => {
            let item = {};
            item.label = ele[0].length === 3 ? ele[0]+"等" : ele[0];
            item.value = ele;
            res.push(item);
        });
        return res;
    }

    handleGenerate = () => {
        axios.get(InitAPI).then((response) => {
            const resData = response.data;
            this.setState({ 
                likeOptions: this.handleOptions(resData.like), 
                candoOptions: this.handleOptions(resData.cando)});
            }).catch((err) => {
                console.log(err);
            });
    }

    componentDidMount = () => {
        this.handleGenerate();
    }

    onDutyChange = (checkedValues) => {
        this.setState({duty: checkedValues});
    }

    onRequireChange = (checkedValues) => {
        this.setState({ require: checkedValues });
    }

    onNext = () => {
        if (this.state.duty.length === 0) {
            message.warning("请选择至少一个词。");
            return;
        } else {
            this.setState({ isNext: false });
        }
    }

    onSubmit = () => {
        if (this.state.require.length === 0) {
            message.warning("请选择至少一个词。");
            return;
        } else {
            const { duty, require } = this.state;
            router.push({
                pathname: '/submit',
                state: { duty: duty, require: require }
            });
        }
    }

    render() {
        return (
            <div>
                <Dsiplay {...this}/>
            </div>
        );
    }
}
export default UserSelect;

