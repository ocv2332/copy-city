import { useEffect, useState } from 'react';
import { RefreshCw } from 'lucide-react';
import { authApi, authStore, backendApi } from './api';
import { AdminPanel } from './admin/adminPanel';
import { MenuBar } from './MenuBar';
import { AboutSection } from './components/AboutSection';
import { AuthPanel } from './components/AuthPanel';
import { Cart } from './components/Cart';
import { Catalog } from './components/Catalog';
import { MapSection } from './components/MapSection';
import { Orders } from './components/Orders';
import { PhotoPrintingSection } from './components/PhotoPrintingSection';
import { ReviewsSection } from './components/ReviewsSection';
import { ServicesMenu } from './components/ServicesMenu';
import type { CartItem, Order, Product, User } from './types';

export function App() {
  const [user, setUser] = useState<User | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const isAdmin = user?.role === 'admin';

  async function loadProducts() {
    setProducts(await backendApi.getProducts());
  }

  async function loadOrders() {
    if (!authStore.getToken()) return;
    setOrders(await backendApi.getOrders());
  }

  async function bootstrap() {
    setLoading(true);
    setError('');
    try {
      await loadProducts();
      if (authStore.getToken()) {
        setUser(await authApi.check());
        await loadOrders();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка загрузки приложения');
      authStore.clear();
      setUser(null);
    } finally {
      setLoading(false);
    }
  }

  async function logout() {
    await authApi.logout();
    setUser(null);
    setOrders([]);
    setCart([]);
  }

  useEffect(() => {
    void bootstrap();
  }, []);

  if (loading) {
    return <div className="screen-state"><RefreshCw className="spin" /> Загружаем кабинет...</div>;
  }

  return (
    <main className="app-shell">
      <MenuBar user={user} onLogout={logout} />

      {error && <p className="error banner">{error}</p>}

      {!user ? (
        <>
          <AuthPanel onAuthorized={(authorizedUser) => {
            setUser(authorizedUser);
            void loadOrders();
          }} />
           <Catalog products={products} cart={cart} setCart={setCart} isAdmin={false} reloadProducts={() => void loadProducts()} />
          <ServicesMenu />
          <PhotoPrintingSection />
          <AboutSection />
          <MapSection />
          <ReviewsSection />
        </>
      ) : (
        <>
  
    
          {isAdmin && <AdminPanel onProductCreated={() => void loadProducts()} />}
          <div className="workspace">
            <div className="main-column">
              <Catalog products={products} cart={cart} setCart={setCart} isAdmin={isAdmin} reloadProducts={() => void loadProducts()} />
              <Orders orders={orders} isAdmin={isAdmin} reloadOrders={() => void loadOrders()} />
            </div>
            <Cart cart={cart} setCart={setCart} onOrderCreated={() => void loadOrders()} />
          </div>
          <ServicesMenu />
          <PhotoPrintingSection />
          <AboutSection />
          <MapSection />
          <ReviewsSection />
        </>
      )}
    </main>
  );
}
