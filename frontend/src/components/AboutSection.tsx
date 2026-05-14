import { Box, Paper, Typography } from '@mui/material';

export function AboutSection() {
  return (
    <Paper className="about-section" component="section" elevation={0} id="about">
      <Box className="about-content">
        <Typography className="eyebrow">О нас</Typography>
        <Typography component="h2">Копир Город помогает быстро оформить печатные задачи без лишних звонков</Typography>
        <Typography>
          Клиент выбирает услуги, собирает заказ и отслеживает статус в личном кабинете. Администратор
          добавляет позиции, фотографии, обновляет статусы и управляет доступом.
        </Typography>
      </Box>
      <Box className="about-stats">
        <Paper elevation={0}>
          <Typography component="strong">24/7</Typography>
          <Typography component="span">заявка через сайт</Typography>
        </Paper>
        <Paper elevation={0}>
          <Typography component="strong">PDF/JPG</Typography>
          <Typography component="span">печать и скан</Typography>
        </Paper>
      </Box>
    </Paper>
  );
}
