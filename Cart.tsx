import { useMemo, useState } from 'react';
import { Box, Button, Paper, TextField, Typography } from '@mui/material';
import { CheckCircle2, ShoppingCart } from 'lucide-react';
import { backendApi } from '../api';
import type { CartItem } from '../types';
import { money } from '../utils/money';

interface CartProps {
  cart: CartItem[];
  setCart: (cart: CartItem[]) => void;
  onOrderCreated: () => void;
}

export function Cart({ cart, setCart, onOrderCreated }: CartProps) {
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(false);
  const total = useMemo(() => cart.reduce((sum, item) => sum + Number(item.base_price) * item.quantity, 0), [cart]);

  function changeQuantity(id: string, quantity: number) {
    if (quantity < 1) {
      setCart(cart.filter((item) => item.id !== id));
      return;
    }
    setCart(cart.map((item) => (item.id === id ? { ...item, quantity } : item)));
  }

  async function submitOrder() {
    setLoading(true);
    try {
      await backendApi.createOrder(cart, comment);
      setCart([]);
      setComment('');
      onOrderCreated();
    } finally {
      setLoading(false);
    }
  }

  return (
    <Paper className="side-panel" component="aside" elevation={0}>
      <Box className="flex flex-row items-center gap-2">
        <ShoppingCart size={20} />
        <Typography className="!text-xl !font-black" component="h2">Корзина</Typography>
      </Box>
      {cart.length === 0 ? (
        <Typography className="!text-slate-500">Добавьте услугу из каталога.</Typography>
      ) : (
        <Box className="grid gap-4">
          <Box className="grid gap-3">
            {cart.map((item) => (
              <Paper className="cart-item" elevation={0} key={item.id}>
                <Box>
                  <Typography className="!font-extrabold">{item.name}</Typography>
                  <Typography className="!text-[13px] !text-slate-500">{money(item.base_price)}</Typography>
                </Box>
                <TextField
                  className="w-20"
                  size="small"
                  type="number"
                  value={item.quantity}
                  onChange={(event) => changeQuantity(item.id, Number(event.target.value))}
                />
              </Paper>
            ))}
          </Box>
          <TextField
            multiline
            minRows={3}
            label="Комментарий к заказу"
            value={comment}
            onChange={(event) => setComment(event.target.value)}
          />
          <Box className="flex flex-row justify-between gap-3">
            <Typography className="!text-slate-500">Итого</Typography>
            <Typography className="!font-black">{money(total)}</Typography>
          </Box>
          <Button className="!font-extrabold" disabled={loading} onClick={submitOrder} startIcon={<CheckCircle2 size={18} />} variant="contained">
            {loading ? 'Оформляем...' : 'Оформить заказ'}
          </Button>
        </Box>
      )}
    </Paper>
  );
}
