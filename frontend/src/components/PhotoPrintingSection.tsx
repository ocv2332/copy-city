import { Box, Button, Card, CardContent, Chip, Paper, Typography } from '@mui/material';
import { ArrowRight, BadgeCheck, Images, Layers, MessageCircle, Ruler } from 'lucide-react';
import { paperOptions, photoSizes } from '../entitis/pageInfo';

export function PhotoPrintingSection() {
  function openReviewForm() {
    window.dispatchEvent(new Event('copy-city:open-review-form'));
    window.location.hash = 'reviews';
  }

  return (
    <Paper className="photo-print-section" component="section" elevation={0}>
      <Box className="photo-print-head flex flex-col items-start gap-4 md:flex-row md:items-center">
        <Box>
          <Typography className="eyebrow">Фотопечать</Typography>
          <Typography className="!text-3xl !font-black !leading-tight !text-pink-700" component="h2">Популярные размеры печати фотографий</Typography>
        </Box>
        <Button className="!font-extrabold" endIcon={<ArrowRight size={16} />} href="#catalog" variant="text">
          Перейти в каталог
        </Button>
      </Box>

      <Box className="photo-size-row">
        {photoSizes.map((item, index) => (
          <Card className={`photo-size-card tone-${item.tone}`} elevation={0} key={item.size}>
            <Box className="photo-scene">
              <Box className="photo-paper primary-photo" />
              <Box className="photo-paper back-photo" />
              <Chip className="!bg-pink-600 !font-black !text-white" label={String(index + 1).padStart(2, '0')} size="small" />
            </Box>
            <CardContent className="!p-1">
              <Typography className="!font-black">{item.size}</Typography>
              <Typography className="!text-xs !text-slate-500">{item.title}</Typography>
            </CardContent>
          </Card>
        ))}
      </Box>

      <Box className="paper-section">
        <Paper className="paper-copy" elevation={0}>
          <Typography className="eyebrow">Бумага</Typography>
          <Typography className="!text-3xl !font-black !leading-tight !text-pink-700" component="h2">На какой бумаге можно печатать фотографии</Typography>
          <Typography className="!text-slate-500">
            Подберите вариант под задачу: быстрый комплект фото, подарок в рамку или печать для
            документов. Карточки можно связать с реальными товарами из backend.
          </Typography>
          <Box className="paper-list grid gap-3">
            {paperOptions.map((option) => (
              <Box className="flex flex-row items-start gap-3" key={option.title}>
                <BadgeCheck size={18} />
                <Box>
                  <Typography className="!font-black">{option.title}</Typography>
                  <Typography className="!text-sm !text-slate-500">{option.text}</Typography>
                </Box>
              </Box>
            ))}
          </Box>
        </Paper>
        <Paper className="paper-preview" elevation={0} aria-label="Примеры печати фотографий">
          <Box className="desk-photo photo-a" />
          <Box className="desk-photo photo-b" />
          <Box className="desk-photo photo-c" />
          <Box className="desk-photo photo-d" />
          <Box className="camera-shape" />
        </Paper>
      </Box>

      <Box className="photo-benefits">
        <Paper className="benefit-card" elevation={0}>
          <Ruler size={24} />
          <Typography className="!font-black">Точные размеры</Typography>
          <Typography className="!text-sm !text-slate-500">Горизонтальные и вертикальные форматы без лишних полей.</Typography>
        </Paper>
        <Paper className="benefit-card highlight" elevation={0}>
          <Images size={24} />
          <Typography className="!font-black">От 10x15 до 30x30</Typography>
          <Typography className="!text-sm !text-slate-500">Подходит для альбомов, рамок, подарков и портфолио.</Typography>
        </Paper>
        <Paper className="benefit-card" elevation={0}>
          <Layers size={24} />
          <Typography className="!font-black">Матовая и глянцевая</Typography>
          <Typography className="!text-sm !text-slate-500">Несколько типов бумаги под разные сценарии печати.</Typography>
        </Paper>
      </Box>

      <Box className="flex flex-col gap-3 rounded-lg border border-pink-100 bg-pink-50 p-5 md:flex-row md:items-center md:justify-between">
        <Box>
          <Typography className="!text-xl !font-black !text-slate-950">Уже печатали фото у нас?</Typography>
          <Typography className="!text-slate-500">Оставьте отзыв, а посмотреть все отзывы можно внизу страницы.</Typography>
        </Box>
        <Button className="!font-extrabold" onClick={openReviewForm} startIcon={<MessageCircle size={17} />} type="button" variant="contained">
          Оставить отзыв
        </Button>
      </Box>
    </Paper>
  );
}
