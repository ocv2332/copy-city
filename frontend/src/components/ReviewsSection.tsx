import { useEffect, useMemo, useState } from 'react';
import { Alert, Box, Button, Chip, Paper, Rating, TextField, Typography } from '@mui/material';
import { MessageCircle } from 'lucide-react';

const REVIEWS_STORAGE_KEY = 'copy_city_photo_reviews';

interface PhotoReview {
  id: string;
  name: string;
  rating: number;
  text: string;
  createdAt: string;
}

const defaultReviews: PhotoReview[] = [
  {
    id: 'default-1',
    name: 'Анна',
    rating: 5,
    text: 'Печатала семейные фотографии 10x15. Цвета получились яркие, заказ быстро подготовили.',
    createdAt: '2026-05-01T10:00:00.000Z',
  },
  {
    id: 'default-2',
    name: 'Максим',
    rating: 5,
    text: 'Удобно, что можно собрать заказ на сайте. Для альбома качество фото подошло отлично.',
    createdAt: '2026-05-03T12:30:00.000Z',
  },
];

function readStoredReviews(): PhotoReview[] {
  const raw = localStorage.getItem(REVIEWS_STORAGE_KEY);
  if (!raw) return defaultReviews;

  try {
    const parsed = JSON.parse(raw) as PhotoReview[];
    return Array.isArray(parsed) ? parsed : defaultReviews;
  } catch {
    return defaultReviews;
  }
}

export function ReviewsSection() {
  const [reviews, setReviews] = useState<PhotoReview[]>([]);
  const [reviewName, setReviewName] = useState('');
  const [reviewText, setReviewText] = useState('');
  const [reviewRating, setReviewRating] = useState<number | null>(5);
  const [reviewSaved, setReviewSaved] = useState(false);
  const [formVisible, setFormVisible] = useState(false);

  useEffect(() => {
    setReviews(readStoredReviews());
  }, []);

  useEffect(() => {
    if (reviews.length > 0) {
      localStorage.setItem(REVIEWS_STORAGE_KEY, JSON.stringify(reviews));
    }
  }, [reviews]);

  useEffect(() => {
    function openReviewForm() {
      setFormVisible(true);
      setReviewSaved(false);
    }

    window.addEventListener('copy-city:open-review-form', openReviewForm);
    return () => window.removeEventListener('copy-city:open-review-form', openReviewForm);
  }, []);

  const averageRating = useMemo(() => {
    if (reviews.length === 0) return 0;
    const total = reviews.reduce((sum, review) => sum + review.rating, 0);
    return Number((total / reviews.length).toFixed(1));
  }, [reviews]);

  function submitReview(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!reviewName.trim() || !reviewText.trim() || !reviewRating) return;

    const review: PhotoReview = {
      id: crypto.randomUUID(),
      name: reviewName.trim(),
      rating: reviewRating,
      text: reviewText.trim(),
      createdAt: new Date().toISOString(),
    };

    setReviews((current) => [review, ...current]);
    setReviewName('');
    setReviewText('');
    setReviewRating(5);
    setReviewSaved(true);
    setFormVisible(false);
  }

  return (
    <Paper className="reviews-page-section" component="section" elevation={0} id="reviews">
      <Box className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <Box>
          <Typography className="eyebrow">Отзывы</Typography>
          <Typography className="!text-3xl !font-black !leading-tight !text-slate-950" component="h2">
            Отзывы клиентов о фотопечати
          </Typography>
          <Typography className="!mt-2 !max-w-2xl !text-slate-500">
            Отзывы сохраняются в браузере и будут доступны после перезагрузки страницы на этом устройстве.
          </Typography>
        </Box>
        <Box className="flex flex-col gap-2 md:items-end">
          <Rating readOnly value={averageRating} precision={0.1} />
          <Typography className="!text-3xl !font-black !text-slate-950">{averageRating || '5.0'}</Typography>
          <Chip className="!bg-amber-100 !font-bold !text-amber-700" label={`${reviews.length} отзывов`} />
        </Box>
      </Box>

      <Box className="reviews-layout">
        <Box className="reviews-list">
          {reviews.map((review) => (
            <Paper className="review-card" elevation={0} key={review.id}>
              <Box className="flex flex-row items-start justify-between gap-3">
                <Box>
                  <Typography className="!font-black !text-slate-950">{review.name}</Typography>
                  <Typography className="!text-xs !text-slate-500">
                    {new Date(review.createdAt).toLocaleDateString('ru-RU')}
                  </Typography>
                </Box>
                <Rating readOnly size="small" value={review.rating} />
              </Box>
              <Typography className="!text-sm !leading-6 !text-slate-600">{review.text}</Typography>
            </Paper>
          ))}
        </Box>

        <Paper className="review-form-card" elevation={0}>
          <Button
            className="!font-extrabold"
            fullWidth
            onClick={() => {
              setFormVisible((visible) => !visible);
              setReviewSaved(false);
            }}
            startIcon={<MessageCircle size={17} />}
            variant="contained"
          >
            {formVisible ? 'Скрыть форму' : 'Оставить отзыв'}
          </Button>

          {formVisible && (
            <Box className="grid gap-3" component="form" onSubmit={submitReview}>
              <TextField
                required
                label="Ваше имя"
                value={reviewName}
                onChange={(event) => setReviewName(event.target.value)}
              />
              <Box className="grid gap-1">
                <Typography className="!text-sm !font-bold !text-slate-600">Оценка</Typography>
                <Rating value={reviewRating} onChange={(_, value) => setReviewRating(value)} />
              </Box>
              <TextField
                required
                multiline
                minRows={4}
                label="Текст отзыва"
                value={reviewText}
                onChange={(event) => setReviewText(event.target.value)}
              />
              <Button className="!font-extrabold" type="submit" variant="contained">
                Сохранить отзыв
              </Button>
            </Box>
          )}

          {reviewSaved && <Alert severity="success">Спасибо! Отзыв сохранен.</Alert>}
        </Paper>
      </Box>
    </Paper>
  );
}
