import type { FormEvent } from 'react';
import { useState } from 'react';
import {
  Alert,
  Box,
  Button,
  Checkbox,
  FormControl,
  FormControlLabel,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  TextField,
  Typography,
} from '@mui/material';
import { PackagePlus, ShieldCheck } from 'lucide-react';
import { authApi, backendApi } from '../api';
import { unitLabels, units } from '../entitis/pageInfo';
import type { CreateProductPayload, ProductUnit, UserRole } from '../types';

interface AdminPanelProps {
  onProductCreated: () => void;
}

interface RoleForm {
  userId: string;
  role: UserRole;
}

export function AdminPanel({ onProductCreated }: AdminPanelProps) {
  const [product, setProduct] = useState<CreateProductPayload>({
    name: '',
    description: '',
    base_price: '',
    unit: 'piece',
    is_active: true,
  });
  const [roleForm, setRoleForm] = useState<RoleForm>({ userId: '', role: 'user' });
  const [message, setMessage] = useState('');

  async function createProduct(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await backendApi.createProduct({
      ...product,
      description: product.description || null,
    });
    setProduct({ name: '', description: '', base_price: '', unit: 'piece', is_active: true });
    setMessage('Товар создан');
    onProductCreated();
  }

  async function updateRole(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const user = await authApi.updateUserRole(roleForm.userId, roleForm.role);
    setMessage(`Роль пользователя ${user.email} изменена на ${user.role}`);
  }

  return (
    <Box className="mb-[30px]" component="section">
      <Paper className="section-head" elevation={0}>
        <Box>
          <Typography className="eyebrow">Admin</Typography>
          <Typography className="!text-2xl !font-black !text-slate-950" component="h2">Панель администратора</Typography>
        </Box>
        <ShieldCheck size={28} />
      </Paper>

      <Box className="admin-grid">
        <Paper className="tool-card grid gap-4" component="form" elevation={0} onSubmit={createProduct}>
          <Typography className="flex items-center gap-2 !text-xl !font-black" component="h3">
            <PackagePlus size={19} /> Новая услуга
          </Typography>
          <TextField required label="Название" value={product.name} onChange={(event) => setProduct({ ...product, name: event.target.value })} />
          <TextField multiline minRows={3} label="Описание" value={product.description || ''} onChange={(event) => setProduct({ ...product, description: event.target.value })} />
          <TextField required label="Цена" type="number" value={product.base_price} onChange={(event) => setProduct({ ...product, base_price: event.target.value })} />
          <FormControl>
            <InputLabel id="product-unit-label">Единица</InputLabel>
            <Select
              label="Единица"
              labelId="product-unit-label"
              value={product.unit}
              onChange={(event) => setProduct({ ...product, unit: event.target.value as ProductUnit })}
            >
              {units.map((unit) => <MenuItem key={unit} value={unit}>{unitLabels[unit]}</MenuItem>)}
            </Select>
          </FormControl>
          <FormControlLabel
            control={<Checkbox checked={product.is_active} onChange={(event) => setProduct({ ...product, is_active: event.target.checked })} />}
            label="Активная услуга"
          />
          <Button className="!font-extrabold" startIcon={<PackagePlus size={18} />} type="submit" variant="contained">Добавить</Button>
        </Paper>

        <Paper className="tool-card grid gap-4" component="form" elevation={0} onSubmit={updateRole}>
          <Typography className="flex items-center gap-2 !text-xl !font-black" component="h3">
            <ShieldCheck size={19} /> Права доступа
          </Typography>
          <TextField required label="ID пользователя" value={roleForm.userId} onChange={(event) => setRoleForm({ ...roleForm, userId: event.target.value })} />
          <FormControl>
            <InputLabel id="role-label">Роль</InputLabel>
            <Select
              label="Роль"
              labelId="role-label"
              value={roleForm.role}
              onChange={(event) => setRoleForm({ ...roleForm, role: event.target.value as UserRole })}
            >
              <MenuItem value="user">user</MenuItem>
              <MenuItem value="admin">admin</MenuItem>
            </Select>
          </FormControl>
          <Button className="!font-extrabold" startIcon={<ShieldCheck size={18} />} type="submit" variant="contained">Сохранить роль</Button>
        </Paper>
      </Box>
      {message && <Alert className="mt-4" severity="success">{message}</Alert>}
    </Box>
  );
}
