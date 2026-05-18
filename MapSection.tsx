import { Box, Chip, Paper, Typography } from '@mui/material';
import { MapPin } from 'lucide-react';

export function MapSection() {
  return (
    <Paper className="map-section" component="section" elevation={0} id="map">
      <Box className="map-info">
        <Typography className="eyebrow">Город Королев</Typography>
        <Typography className="!text-3xl !font-black !leading-tight !text-slate-950" component="h2">Работаем для жителей Королева</Typography>
        <Typography className="!text-slate-500">
          На карте отмечен город Королев. Точный адрес точки можно будет заменить в одном месте,
          когда появится финальная локация копицентра.
        </Typography>
        <Chip className="!justify-self-start !bg-blue-100 !font-bold !text-blue-700" icon={<MapPin size={18} />} label="Московская область, Королев" />
      </Box>
      <iframe
        className="city-map"
        src="https://yandex.ru/map-widget/v1/?ll=37.854629%2C55.922212&z=12&pt=37.854629%2C55.922212%2Cpm2rdm"
        title="Карта города Королева"
        loading="lazy"
      />
    </Paper>
  );
}
