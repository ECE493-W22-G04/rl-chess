import React, { useState } from 'react';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';

import AuthService from '../services/auth';

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
        <div className="col-md-12">
            <div className="card card-container">
                <Formik initialValues={initialValues} validationSchema={validationSchema} onSubmit={handleLogin}>
                    <Form>
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
                            <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
                                {loading && <span className="spinner-border spinner-border-sm"></span>}
                                <span>Login</span>
                            </button>
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
            </div>
        </div>
    );
};

export default Login;
