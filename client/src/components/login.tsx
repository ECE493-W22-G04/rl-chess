import React, { useState } from 'react';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

import AuthService from '../services/auth';

// This File is used to satisfy the following functional requirements:
// FR4 - User.Login

const Login: React.FunctionComponent = () => {
    const [loading, setLoading] = useState<boolean>(false);
    const [message, setMessage] = useState<string>('');

    const validationSchema = () => {
        return Yup.object().shape({
            email: Yup.string().required('This field is required!'),
            password: Yup.string().required('This field is required!'),
        });
    };

    const handleLogin = (formValue: { email: string; password: string }) => {
        const { email, password } = formValue;

        setMessage('');
        setLoading(true);

        AuthService.login(email, password).then(
            () => {
                // Move to Home page
                // TODO: Manage navigating to a game
                window.location.assign('/');
            },
            (error) => {
                const resMessage = (error.response && error.response.data && error.response.data.message) || error.message || error.toString();

                setMessage(resMessage);
                setLoading(false);
            }
        );
    };

    const initialValues = {
        email: '',
        password: '',
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'center' }}>
            <Card style={{ width: '30em' }}>
                <Formik initialValues={initialValues} validationSchema={validationSchema} onSubmit={handleLogin}>
                    <Form style={{ margin: '1em' }}>
                        <div className="form-group">
                            <label htmlFor="email">Email</label>
                            <Field name="email" type="text" className="form-control" />
                            <ErrorMessage name="email" component="div" className="alert alert-danger" />
                        </div>

                        <div className="form-group">
                            <label htmlFor="password">Password</label>
                            <Field name="password" type="password" className="form-control" />
                            <ErrorMessage name="password" component="div" className="alert alert-danger" />
                        </div>

                        <div className="form-group">
                            <Button type="submit" disabled={loading}>
                                {loading && <span className="spinner-border spinner-border-sm"></span>}
                                <span>Login</span>
                            </Button>
                        </div>

                        {message && (
                            <div className="form-group">
                                <div className="alert alert-danger" role="alert">
                                    {message}
                                </div>
                            </div>
                        )}
                    </Form>
                </Formik>
            </Card>
        </div>
    );
};

export default Login;
