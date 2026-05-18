import type { FormEvent } from 'react';
import { useState } from 'react';
import { Alert, Box, Button, Paper, Tab, Tabs, TextField, Typography } from '@mui/material';
import { LogIn, UserPlus } from 'lucide-react';
import { authApi } from '../api';
import type { RegisterPayload, User } from '../types';

interface AuthPanelProps {
  onAuthorized: (user: User) => void;
}

interface LoginForm {
  email: string;
  password: string;
}

type RegisterForm = Omit<RegisterPayload, 'middle_name'> & {
  middle_name: string;
};

export function AuthPanel({ onAuthorized }: AuthPanelProps) {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [loginForm, setLoginForm] = useState<LoginForm>({ email: '', password: '' });
  const [registerForm, setRegisterForm] = useState<RegisterForm>({
    email: '',
    lastname: '',
    firstname: '',
    middle_name: '',
    date_of_birth: '',
    password: '',
  });

  async function submitLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError('');
    try {
      await authApi.login(loginForm.email, loginForm.password);
      onAuthorized(await authApi.check());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка входа');
    } finally {
      setLoading(false);
    }
  }

  async function submitRegister(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError('');
    try {
      await authApi.register({
        ...registerForm,
        middle_name: registerForm.middle_name || null,
      });
      await authApi.login(registerForm.email, registerForm.password);
      onAuthorized(await authApi.check());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка регистрации');
    } finally {
      setLoading(false);
    }
  }

  return (
    <Box className="auth-panel" component="section">
      <Box className="auth-copy">
        <Typography className="eyebrow">Копир Город</Typography>
        <Typography className="!mb-4 !max-w-3xl !text-4xl !font-black !leading-tight md:!text-5xl" component="h1">
          Печать, фото и заказы в одном рабочем кабинете
        </Typography>
        <Typography className="!max-w-2xl !text-base !leading-7 !text-white/80">
          Пользователь оформляет заказы и отслеживает статусы. Администратор добавляет услуги,
          фотографии, меняет статусы и права доступа.
        </Typography>
      </Box>

      <Paper className="auth-card" elevation={0}>
        <Tabs className="mb-4 rounded-lg bg-slate-100" value={mode} onChange={(_, value: 'login' | 'register') => setMode(value)} variant="fullWidth">
          <Tab icon={<LogIn size={18} />} iconPosition="start" label="Вход" value="login" />
          <Tab icon={<UserPlus size={18} />} iconPosition="start" label="Регистрация" value="register" />
        </Tabs>

        {mode === 'login' ? (
          <Box className="grid gap-4" component="form" onSubmit={submitLogin}>
            <TextField
              required
              label="Email"
              type="email"
              value={loginForm.email}
              onChange={(event) => setLoginForm({ ...loginForm, email: event.target.value })}
              placeholder="user@gmail.com"
            />
            <TextField
              required
              label="Пароль"
              type="password"
              value={loginForm.password}
              onChange={(event) => setLoginForm({ ...loginForm, password: event.target.value })}
              placeholder="Password1!"
            />
            <Button className="!py-3 !font-extrabold" disabled={loading} startIcon={<LogIn size={18} />} type="submit" variant="contained">
              {loading ? 'Входим...' : 'Войти'}
            </Button>
          </Box>
        ) : (
          <Box className="grid gap-4 sm:grid-cols-2" component="form" onSubmit={submitRegister}>
            <TextField required label="Фамилия" value={registerForm.lastname} onChange={(event) => setRegisterForm({ ...registerForm, lastname: event.target.value })} />
            <TextField required label="Имя" value={registerForm.firstname} onChange={(event) => setRegisterForm({ ...registerForm, firstname: event.target.value })} />
            <TextField label="Отчество" value={registerForm.middle_name} onChange={(event) => setRegisterForm({ ...registerForm, middle_name: event.target.value })} />
            <TextField required label="Дата рождения" type="date" value={registerForm.date_of_birth} onChange={(event) => setRegisterForm({ ...registerForm, date_of_birth: event.target.value })} />
            <TextField required label="Email" type="email" value={registerForm.email} onChange={(event) => setRegisterForm({ ...registerForm, email: event.target.value })} placeholder="user@gmail.com" />
            <TextField required label="Пароль" type="password" value={registerForm.password} onChange={(event) => setRegisterForm({ ...registerForm, password: event.target.value })} placeholder="Password1!" />
            <Button className="!py-3 !font-extrabold sm:col-span-2" disabled={loading} startIcon={<UserPlus size={18} />} type="submit" variant="contained">
              {loading ? 'Создаем...' : 'Создать аккаунт'}
            </Button>
          </Box>
        )}

        {error && <Alert className="mt-4" severity="error">{error}</Alert>}
      </Paper>
    </Box>
  );
}
