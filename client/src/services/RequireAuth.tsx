import React, { FC } from 'react';
import { Navigate } from 'react-router-dom';

import AuthService from '../services/auth';

interface RequireAuthProps {
    children: JSX.Element;
}

const RequireAuth: FC<RequireAuthProps> = ({ children }: RequireAuthProps) => {
    if (AuthService.getCurrentUser() === null) {
        return <Navigate to="/login" />;
    }
    return children;
};

export default RequireAuth;
