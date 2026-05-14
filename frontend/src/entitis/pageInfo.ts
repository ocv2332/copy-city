import type { LucideIcon } from 'lucide-react';
import { ClipboardList, FileText, Image, Palette, Printer, ScanLine } from 'lucide-react';
import type { OrderStatus, ProductUnit } from '../types';

export const units: ProductUnit[] = ['page', 'piece', 'photo', 'order', 'hour'];

export const unitLabels: Record<ProductUnit, string> = {
  page: 'страница',
  piece: 'штука',
  photo: 'фото',
  order: 'заказ',
  hour: 'час',
};

export const statuses: OrderStatus[] = ['new', 'in_progress', 'done', 'cancelled'];

export const statusLabels: Record<OrderStatus, string> = {
  new: 'Новый',
  in_progress: 'В работе',
  done: 'Готов',
  cancelled: 'Отменен',
};

export interface ServiceMenuItem {
  icon: LucideIcon;
  title: string;
  text: string;
}

export const serviceMenu: ServiceMenuItem[] = [
  {
    icon: Printer,
    title: 'Печать документов',
    text: 'Черно-белая и цветная печать, срочные тиражи, печать учебных и рабочих материалов.',
  },
  {
    icon: FileText,
    title: 'Копирование',
    text: 'Копии паспортов, договоров, заявлений, методичек и комплектов документов.',
  },
  {
    icon: ScanLine,
    title: 'Сканирование',
    text: 'Скан в PDF/JPG, многостраничные файлы, отправка на почту или сохранение на носитель.',
  },
  {
    icon: Image,
    title: 'Фотоуслуги',
    text: 'Печать фотографий, подготовка фото на документы, базовая ретушь и кадрирование.',
  },
  {
    icon: Palette,
    title: 'Дизайн и макеты',
    text: 'Визитки, листовки, сертификаты, подготовка файлов к аккуратной печати.',
  },
  {
    icon: ClipboardList,
    title: 'Сборные заказы',
    text: 'Несколько услуг в одном заказе с комментариями, статусами и личным кабинетом.',
  },
];

export type PhotoSizeTone = 'coral' | 'blue' | 'green' | 'amber';

export interface PhotoSizeCardInfo {
  size: string;
  title: string;
  tone: PhotoSizeTone;
}

export const photoSizes: PhotoSizeCardInfo[] = [
  { size: '10x15', title: 'Классический снимок', tone: 'coral' },
  { size: '15x21', title: 'Для рамки и альбома', tone: 'blue' },
  { size: 'A4', title: 'Постер на стену', tone: 'green' },
  { size: 'A3', title: 'Большой формат', tone: 'amber' },
];

export interface PaperOption {
  title: string;
  text: string;
}

export const paperOptions: PaperOption[] = [
  {
    title: 'Стандарт',
    text: 'Матовая или глянцевая фотобумага для семейных снимков, учебных проектов и альбомов.',
  },
  {
    title: 'Премиум',
    text: 'Более плотная бумага для подарочных фотографий, портфолио и интерьерной печати.',
  },
  {
    title: 'Документная',
    text: 'Аккуратная печать фото на документы с подготовкой под нужный формат.',
  },
];
