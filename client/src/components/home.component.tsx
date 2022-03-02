import React, { Component } from 'react';
import UserService from '../services/user.service';
type Props = Record<string, unknown>;
type State = {
    content: string;
};
export default class Home extends Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = {
            content: '',
        };
    }
    componentDidMount() {
        const tokenStr = localStorage.getItem('token');
        if (!tokenStr) {
            UserService.getPublicContent().then(
                (response) => {
                    this.setState({
                        content: response.data.message,
                    });
                },
                (error) => {
                    this.setState({
                        content:
                            (error.response && error.response.data) ||
                            error.message ||
                            error.toString(),
                    });
                }
            );
        } else {
            UserService.getUserBoard().then(
                (response) => {
                    this.setState({
                        content: response.data.message,
                    });
                },
                (error) => {
                    this.setState({
                        content:
                            (error.response && error.response.data) ||
                            error.message ||
                            error.toString(),
                    });
                }
            );
        }
    }
    render() {
        return (
            <div className="container">
                <header className="jumbotron">
                    <h3>{this.state.content}</h3>
                </header>
            </div>
        );
    }
}
