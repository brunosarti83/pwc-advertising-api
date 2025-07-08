import { Navigate, Outlet, useRoutes } from 'react-router-dom'
import AuthLayout from './layouts/AuthLayout'
import MainLayout from './layouts/MainLayout'
import BillboardsView from './views/BillboardsView'
import CampaignBillboardsView from './views/CampaignBillboardsView'
import CampaignsView from './views/CampaignsView'
import LocationsView from './views/LocationsView'
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
            { path: '/campaigns', element: <CampaignsView /> },
            { path: '/billboards', element: <BillboardsView /> },
            { path: '/locations', element: <LocationsView /> },
            { path: '/campaign-billboards/:id', element: <CampaignBillboardsView /> },
          ]
        },
    ])
}

export default Routes