export type UserRole = 'user' | 'admin';

export type ProductUnit = 'page' | 'piece' | 'photo' | 'order' | 'hour';

export type OrderStatus = 'new' | 'in_progress' | 'done' | 'cancelled';

export interface User {
  id: string;
  email: string;
  lastname: string;
  firstname: string;
  middle_name: string | null;
  date_of_birth: string;
  role: UserRole;
}

export interface RegisterPayload {
  email: string;
  lastname: string;
  firstname: string;
  middle_name: string | null;
  date_of_birth: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface Photo {
  id: string;
  file_name: string;
  mime_type: string;
  file_size: number;
  created_at: string;
  updated_at: string;
}

export interface ProductShort {
  id: string;
  name: string;
  base_price: string | number;
  unit: ProductUnit;
}

export interface Product extends ProductShort {
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  photos: Photo[];
}

export interface CartItem extends Product {
  quantity: number;
}

export interface CreateProductPayload {
  name: string;
  description: string | null;
  base_price: string;
  unit: ProductUnit;
  is_active: boolean;
}

export interface OrderItem {
  id: string;
  product_id: string;
  quantity: number;
  price: string | number;
  total_price: string | number;
  product: ProductShort | null;
}

export interface Order {
  id: string;
  user_id: string;
  status: OrderStatus;
  total_amount: string | number;
  comment: string | null;
  created_at: string;
  updated_at: string;
  items: OrderItem[];
}

export interface ApiValidationError {
  msg?: string;
}

export interface LabeledOption<T extends string = string> {
  value: T;
  label: string;
}
