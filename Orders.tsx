import { useState } from 'react';
import { Box, Chip, FormControl, MenuItem, Paper, Select, Typography } from '@mui/material';
import { backendApi } from '../api';
import { statusLabels, statuses } from '../entitis/pageInfo';
import type { Order, OrderStatus } from '../types';
import { money } from '../utils/money';

interface OrdersProps {
  orders: Order[];
  isAdmin: boolean;
  reloadOrders: () => void;
}

export function Orders({ orders, isAdmin, reloadOrders }: OrdersProps) {
  const [updating, setUpdating] = useState('');

  async function updateStatus(orderId: string, status: OrderStatus) {
    setUpdating(orderId);
    try {
      await backendApi.updateOrderStatus(orderId, status);
      reloadOrders();
    } finally {
      setUpdating('');
    }
  }

  return (
    <Box component="section">
      <Paper className="section-head" elevation={0}>
        <Box>
          <Typography className="eyebrow">История</Typography>
          <Typography className="!text-2xl !font-black !text-slate-950" component="h2">Мои заказы</Typography>
        </Box>
        <Chip className="!bg-blue-100 !font-bold !text-blue-700" label={`${orders.length} заказов`} />
      </Paper>
      <Box className="grid gap-3">
        {orders.length === 0 && (
          <Paper className="empty wide" elevation={0}>
            <Typography className="!text-slate-500">После оформления заказа он появится здесь.</Typography>
          </Paper>
        )}
        {orders.map((order) => (
          <Paper className="order-card" elevation={0} key={order.id}>
            <Box className="flex flex-row items-center justify-between gap-3">
              <Box>
                <Typography className="!font-black">Заказ {order.id.slice(0, 8)}</Typography>
                <Typography className="!text-[13px] !text-slate-500">{new Date(order.created_at).toLocaleString('ru-RU')}</Typography>
              </Box>
              <Chip className={`status-${order.status}`} label={statusLabels[order.status] || order.status} size="small" />
            </Box>
            <Box className="flex flex-row flex-wrap gap-2">
              {order.items?.map((item) => (
                <Chip key={item.id} label={`${item.product?.name || item.product_id} x ${item.quantity}`} size="small" />
              ))}
            </Box>
            <Box className="flex flex-row justify-between gap-3">
              <Typography className="!text-slate-500">{order.comment || 'Без комментария'}</Typography>
              <Typography className="!font-black">{money(order.total_amount)}</Typography>
            </Box>
            {isAdmin && (
              <FormControl className="max-w-56" size="small">
                <Select
                  value={order.status}
                  disabled={updating === order.id}
                  onChange={(event) => updateStatus(order.id, event.target.value as OrderStatus)}
                >
                  {statuses.map((status) => (
                    <MenuItem key={status} value={status}>
                      {statusLabels[status]}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            )}
          </Paper>
        ))}
      </Box>
    </Box>
  );
}
