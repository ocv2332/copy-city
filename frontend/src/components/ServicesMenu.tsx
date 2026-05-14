import { Box, Card, CardContent, Chip, Paper, Typography } from '@mui/material';
import { serviceMenu } from '../entitis/pageInfo';

export function ServicesMenu() {
  return (
    <Box className="services-section" component="section" id="services">
      <Paper className="section-head" elevation={0}>
        <Box>
          <Typography className="eyebrow">Меню услуг</Typography>
          <Typography className="!text-2xl !font-black !text-slate-950" component="h2">Все, что обычно нужно в копицентре</Typography>
        </Box>
        <Chip className="!bg-blue-100 !font-bold !text-blue-700" label={`${serviceMenu.length} направлений`} />
      </Paper>
      <Box className="service-grid">
        {serviceMenu.map((service) => {
          const Icon = service.icon;
          return (
            <Card className="service-card" elevation={0} key={service.title}>
              <CardContent className="grid gap-3 !p-0">
                <Box className="service-icon">
                  <Icon size={24} />
                </Box>
                <Typography className="!text-xl !font-black !text-slate-950" component="h3">{service.title}</Typography>
                <Typography className="!text-slate-500">{service.text}</Typography>
              </CardContent>
            </Card>
          );
        })}
      </Box>
    </Box>
  );
}
