import { useEffect, useState } from 'react';
import { Box, Button, Card, CardContent, Chip, IconButton, Typography } from '@mui/material';
import { Camera, ChevronLeft, ChevronRight, ShoppingCart } from 'lucide-react';
import { backendApi } from '../api';
import { unitLabels } from '../entitis/pageInfo';
import type { Product } from '../types';
import { money } from '../utils/money';

interface ProductCardProps {
  product: Product;
  isAdmin: boolean;
  onAdd: (product: Product) => void;
  onPhotoUploaded: () => void;
}

export function ProductCard({ product, onAdd, isAdmin, onPhotoUploaded }: ProductCardProps) {
  const [file, setFile] = useState<File | null>(null);
  const [currentPhotoIndex, setCurrentPhotoIndex] = useState(0);
  const photos = product.photos || [];
  const currentPhoto = photos[currentPhotoIndex];
  const hasSeveralPhotos = photos.length > 1;

  useEffect(() => {
    setCurrentPhotoIndex(0);
  }, [product.id, photos.length]);

  function showPreviousPhoto() {
    setCurrentPhotoIndex((index) => (index === 0 ? photos.length - 1 : index - 1));
  }

  function showNextPhoto() {
    setCurrentPhotoIndex((index) => (index + 1) % photos.length);
  }

  async function upload() {
    if (!file) return;
    await backendApi.uploadPhoto(product.id, file);
    setFile(null);
    onPhotoUploaded();
  }

  return (
    <Card className="product-card" elevation={0}>
      <Box className="photo-box">
        {currentPhoto ? (
          <>
            <img src={backendApi.getPhotoUrl(currentPhoto.id)} alt={product.name} />
            {hasSeveralPhotos && (
              <>
                <IconButton className="carousel-button previous" onClick={showPreviousPhoto} title="Предыдущее фото">
                  <ChevronLeft size={19} />
                </IconButton>
                <IconButton className="carousel-button next" onClick={showNextPhoto} title="Следующее фото">
                  <ChevronRight size={19} />
                </IconButton>
                <Box className="carousel-dots">
                  {photos.map((photo, index) => (
                    <button
                      aria-label={`Фото ${index + 1}`}
                      className={index === currentPhotoIndex ? 'active' : ''}
                      key={photo.id}
                      onClick={() => setCurrentPhotoIndex(index)}
                      type="button"
                    />
                  ))}
                </Box>
                <Chip className="photo-counter !bg-slate-950/75 !font-bold !text-white" label={`${currentPhotoIndex + 1} / ${photos.length}`} size="small" />
              </>
            )}
          </>
        ) : (
          <Camera size={34} />
        )}
      </Box>
      <CardContent className="product-body">
        <Box>
          <Typography className="!text-xl !font-black !text-slate-950" component="h3">{product.name}</Typography>
          <Typography className="!mt-2 !text-slate-500">{product.description || 'Описание услуги пока не добавлено'}</Typography>
        </Box>
        <Box className="flex flex-row flex-wrap items-center gap-2">
          <Typography className="!text-xl !font-black !text-slate-950">{money(product.base_price)}</Typography>
          <Chip className="!bg-slate-100 !text-slate-600" label={unitLabels[product.unit] || product.unit} size="small" />
          <Chip className={product.is_active ? '!bg-emerald-100 !font-bold !text-emerald-700' : '!bg-slate-100 !font-bold !text-slate-500'} label={product.is_active ? 'Активно' : 'Скрыто'} size="small" />
        </Box>
        <Button className="!font-extrabold" fullWidth onClick={() => onAdd(product)} startIcon={<ShoppingCart size={17} />} variant="outlined">
          В корзину
        </Button>
        {isAdmin && (
          <Box className="flex flex-row items-center gap-2">
            <Button className="!font-bold" component="label" size="small" variant="outlined">
              Выбрать фото
              <input hidden type="file" accept="image/*" onChange={(event) => setFile(event.target.files?.[0] || null)} />
            </Button>
            <IconButton disabled={!file} onClick={upload} title="Загрузить фото">
              <Camera size={18} />
            </IconButton>
          </Box>
        )}
      </CardContent>
    </Card>
  );
}
