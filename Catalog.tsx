import { Box, Chip, Paper, Typography } from '@mui/material';
import type { CartItem, Product } from '../types';
import { ProductCard } from './ProductCard';

interface CatalogProps {
  products: Product[];
  cart: CartItem[];
  setCart: (cart: CartItem[]) => void;
  isAdmin: boolean;
  reloadProducts: () => void;
}

export function Catalog({ products, cart, setCart, isAdmin, reloadProducts }: CatalogProps) {
  function add(product: Product) {
    const current = cart.find((item) => item.id === product.id);
    if (current) {
      setCart(cart.map((item) => (item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item)));
      return;
    }
    setCart([...cart, { ...product, quantity: 1 }]);
  }

  return (
    <Box component="section" id="catalog">
      <Paper className="section-head" elevation={0}>
        <Box>
          <Typography className="eyebrow">Каталог</Typography>
          <Typography className="!text-2xl !font-black !text-slate-950" component="h2">Услуги копицентра</Typography>
        </Box>
        <Chip className="!bg-blue-100 !font-bold !text-blue-700" label={`${products.length} позиций`} />
      </Paper>
      <Box className="products-grid">
        {products.map((product) => (
          <ProductCard
            key={product.id}
            product={product}
            onAdd={add}
            isAdmin={isAdmin}
            onPhotoUploaded={reloadProducts}
          />
        ))}
      </Box>
    </Box>
  );
}
