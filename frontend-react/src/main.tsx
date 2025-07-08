import { HeroUIProvider } from '@heroui/react';
import { ToastProvider } from "@heroui/toast";
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import './index.css';

createRoot(document.getElementById('root')!).render(
  <HeroUIProvider>
    <ToastProvider />
    <App />
  </HeroUIProvider>,
)
