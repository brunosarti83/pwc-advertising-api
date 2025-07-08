import { Navigate, Outlet, useRoutes } from 'react-router-dom'
import AuthLayout from './layouts/AuthLayout'
import MainLayout from './layouts/MainLayout'
import BillboardsView from './views/BillboardsView'
import SigninView from './views/SigninView'
import SignupView from './views/SignupView'

const Routes = () => {
  return useRoutes([
        {
          path: '/auth',
          element: (
              <AuthLayout>
                <Outlet />
              </AuthLayout>
          ),
          children: [
            { path: '/auth/signin', element: <SigninView /> },
            { path: '/auth/signup', element: <SignupView /> },
          ]
        },
        {
          path: '/',
          element: (
            <MainLayout>
                <Outlet />
            </MainLayout>
          ),
          children: [
            { path: '/', element: <Navigate to="/billboards" /> },
            { path: '/billboards', element: <BillboardsView /> },
          ]
        },
    ])
}

export default Routes