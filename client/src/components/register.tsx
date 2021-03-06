import React, { useState } from 'react';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

import AuthService from '../services/auth';

// This File is used to satisfy the following functional requirements:
// FR1 - User.Registration
// FR3 - Email.Validation

const Register: React.FunctionComponent = () => {
    const [successful, setSuccessful] = useState<boolean>(false);
    const [message, setMessage] = useState<string>('');

    const validationSchema = () => {
        return Yup.object().shape({
            email: Yup.string().email('This is not a valid email.').required('This field is required!'),
            password: Yup.string().min(8, 'The password must be between 8 and 40 characters.').max(40, 'The password must be between 8 and 40 characters.').required('This field is required!'),
        });
    };

    const handleRegister = (formValue: { email: string; password: string }) => {
        const { email, password } = formValue;

        setMessage('');
        setSuccessful(false);

        AuthService.register(email, password).then(
            (response) => {
                setMessage(response.data.message);
                setSuccessful(true);
            },
            (error) => {
                const resMessage = (error.response && error.response.data && error.response.data.message) || error.message || error.toString();
                setMessage(resMessage);
                setSuccessful(false);
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
                <Formik initialValues={initialValues} validationSchema={validationSchema} onSubmit={handleRegister}>
                    <Form style={{ margin: '1em' }}>
                        {!successful && (
                            <div>
                                <div className="form-group">
                                    <label htmlFor="email"> Email </label>
                                    <Field name="email" type="email" className="form-control" />
                                    <ErrorMessage name="email" component="div" className="alert alert-danger" />
                                </div>

                                <div className="form-group">
                                    <label htmlFor="password"> Password </label>
                                    <Field name="password" type="password" className="form-control" />
                                    <ErrorMessage name="password" component="div" className="alert alert-danger" />
                                </div>

                                <div className="form-group">
                                    <Button type="submit">Sign Up</Button>
                                </div>
                            </div>
                        )}

                        {message && (
                            <div className="form-group">
                                <div className={successful ? 'alert alert-success' : 'alert alert-danger'} role="alert">
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

export default Register;
