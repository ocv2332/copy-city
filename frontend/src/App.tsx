import { useeffect, usestate } from 'react';
import { refreshcw } from 'lucide-react';
import { authapi, authstore, backendapi } from './api';
import { adminpanel } from './admin/adminpanel';
import { menubar } from './menubar';
import { aboutsection } from './components/aboutsection';
import { authpanel } from './components/authpanel';
import { cart } from './components/cart';
import { catalog } from './components/catalog';
import { mapsection } from './components/mapsection';
import { orders } from './components/orders';
import { photoprintingsection } from './components/photoprintingsection';
import { reviewssection } from './components/reviewssection';
import { servicesmenu } from './components/servicesmenu';
import type { cartitem, order, product, user } from './types';

export function app() {
  const [user, setuser] = usestate<user | null>(null);
  const [products, setproducts] = usestate<product[]>([]);
  const [orders, setorders] = usestate<order[]>([]);
  const [cart, setcart] = usestate<cartitem[]>([]);
  const [loading, setloading] = usestate(true);
  const [error, seterror] = usestate('');

  const isadmin = user?.role === 'admin';

  async function loadproducts() {
    setproducts(await backendapi.getproducts());
  }

  async function loadorders() {
    if (!authstore.gettoken()) return;
    setorders(await backendapi.getorders());
  }

  async function bootstrap() {
    setloading(true);
    seterror('');
    try {
      await loadproducts();
      if (authstore.gettoken()) {
        setuser(await authapi.check());
        await loadorders();
      }
    } catch (err) {
      seterror(err instanceof error ? err.message : 'ошибка загрузки приложения');
      authstore.clear();
      setuser(null);
    } finally {
      setloading(false);
    }
  }

  async function logout() {
    await authapi.logout();
    setuser(null);
    setorders([]);
    setcart([]);
  }

  useeffect(() => {
    void bootstrap();
  }, []);

  if (loading) {
    return <div classname="screen-state"><refreshcw classname="spin" /> загружаем кабинет...</div>;
  }

  return (
    <main classname="app-shell">
      <menubar user={user} onlogout={logout} />

      {error && <p classname="error banner">{error}</p>}

      {!user ? (
        <>
          <authpanel onauthorized={(authorizeduser) => {
            setuser(authorizeduser);
            void loadorders();
          }} />
           <catalog products={products} cart={cart} setcart={setcart} isadmin={false} reloadproducts={() => void loadproducts()} />
          <servicesmenu />
          <photoprintingsection />
          <aboutsection />
          <mapsection />
          <reviewssection />
        </>
      ) : (
        <>


          {isadmin && <adminpanel onproductcreated={() => void loadproducts()} />}
          <div classname="workspace">
            <div classname="main-column">
              <catalog products={products} cart={cart} setcart={setcart} isadmin={isadmin} reloadproducts={() => void loadproducts()} />
              <orders orders={orders} isadmin={isadmin} reloadorders={() => void loadorders()} />
            </div>
            <cart cart={cart} setcart={setcart} onordercreated={() => void loadorders()} />
          </div>
          <servicesmenu />
          <photoprintingsection />
          <aboutsection />
          <mapsection />
          <reviewssection />
        </>
      )}
    </main>
  );
}
