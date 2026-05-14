import { Avatar, Box, Button, Chip, Paper, Typography } from '@mui/material';
import { LogOut } from 'lucide-react';
import type { User } from './types';

interface MenuBarProps {
  user: User | null;
  onLogout: () => void;
}

export function MenuBar({ user, onLogout }: MenuBarProps) {
  return (
    <Paper className="topbar" component="header" elevation={0}>
      <Box className="flex flex-row items-center gap-3">
        <Avatar className="!h-11 !w-11 !rounded-lg !bg-gradient-to-br !from-blue-600 !via-cyan-500 !to-emerald-500 !font-black shadow-lg shadow-blue-500/30" variant="rounded">
          КГ
        </Avatar>
        <Box>
          <Typography className="!font-black !leading-tight !text-slate-950">Копир Город</Typography>
          <Typography className="!text-[13px] !text-slate-500">Личный кабинет</Typography>
        </Box>
      </Box>

      <Box className="site-nav" component="nav">
        <Button className="!font-bold !text-slate-600" href="#services">Услуги</Button>
        <Button className="!font-bold !text-slate-600" href="#catalog">Каталог</Button>
        <Button className="!font-bold !text-slate-600" href="#about">О нас</Button>
        <Button className="!font-bold !text-slate-600" href="#reviews">Отзывы</Button>
        <Button className="!font-bold !text-slate-600" href="#map">Карта</Button>
      </Box>

      {user ? (
        <Box className="user-box flex flex-row items-center gap-3">
          <Chip className={user.role === 'admin' ? '!bg-pink-100 !font-bold !text-pink-700' : '!bg-blue-100 !font-bold !text-blue-700'} label={user.role} size="small" />
          <Box>
            <Typography className="!font-extrabold !leading-tight !text-slate-950">
              {user.firstname} {user.lastname}
            </Typography>
            <Typography className="!text-[13px] !text-slate-500">{user.email}</Typography>
          </Box>
          <Button className="!border-slate-300 !text-slate-700" onClick={onLogout} size="small" startIcon={<LogOut size={18} />} variant="outlined">
            Выйти
          </Button>
        </Box>
      ) : (
        <Chip className="!bg-slate-100 !font-bold !text-slate-500" label="Гость" />
      )}
    </Paper>
  );
}
